"""Client module for downloading shards."""

import os
import time
import threading
import subprocess
from typing import List, Dict, Optional, Set
from concurrent.futures import ThreadPoolExecutor

from shardcast.envs import (
    DISTRIBUTION_FILE,
    HTTP_TIMEOUT,
    MAX_CONCURRENT_DOWNLOADS,
    RETRY_ATTEMPTS,
    FAST_RETRY_ATTEMPTS,
    FAST_RETRY_INTERVAL,
    SLOW_RETRY_INTERVAL,
)
from shardcast.utils import logger, ensure_dir
from pathlib import Path
from collections import namedtuple

# TODO: Use namedtuple instead of dict
ServerMetrics = namedtuple("ServerMetrics", ["bandwidth_mbps", "success_rate"])


class ShardDownloader:
    """Client for downloading shards from servers."""

    def __init__(self, servers: List[str], timeout: int = HTTP_TIMEOUT):
        """Initialize the shard downloader.

        Args:
            servers: List of server URLs or IP addresses
            timeout: Timeout for HTTP requests in seconds
        """
        # TODO: Make this a property of server_metrics. Otherwise we always need to sync them
        self.servers = servers
        self.timeout = timeout
        # Lock for thread-safe access to metrics
        self.metrics_lock = threading.Lock()
        logger.info(f"Initializing shard downloader with servers: {self.servers} and timeout: {self.timeout}")

        # Server performance metrics
        self.server_metrics: Dict[str, Dict[str, float]] = {}
        self._init_server_metrics()

    def _init_server_metrics(self) -> Dict[str, Dict[str, float]]:
        """Initialize server metrics by downloading the distribution file."""
        # TODO: Make file creation automatic for non-leaf nodes
        for server in self.servers:
            tmp_path = Path("/tmp/dummy.bin")
            self._download_file(server, "data1.bin", tmp_path)
            tmp_path.unlink()

    def _get_best_servers(self, num_servers: int = 3) -> List[str]:
        """Get the best servers based on performance metrics.

        Args:
            num_servers: Number of best servers to return

        Returns:
            List of best server URLs
        """
        with self.metrics_lock:
            # Sort servers by: success_rate (desc), speed (desc), latency (asc)
            sorted_servers = sorted(
                self.servers,
                key=lambda s: (
                    -self.server_metrics[s]["success_rate"],
                    -self.server_metrics[s]["bandwidth_mbps"],
                ),
            )

            logger.debug(f"Sorted servers: {sorted_servers}")
            logger.debug(f"Metrics: {self.server_metrics}")

            return sorted_servers[: min(num_servers, len(sorted_servers))]

    def _update_server_metrics(self, server: str, bandwidth_mbps: float, success: bool) -> None:
        """Update performance metrics for a server.

        Args:
            server: Server URL
            bandwidth_mbps: Bandwidth in MB/s
            success: Whether the download was successful
        """
        # TODO: ENV / CONSTANT
        alpha = 0.3
        heal_rate = 0.01
        with self.metrics_lock:
            # Initialize metrics if server is not in metrics
            if server not in self.server_metrics:
                self.server_metrics[server] = {"bandwidth_mbps": bandwidth_mbps, "success_rate": 1.0 if success else 0.0}
                return

            # Otherwise EMA
            self.server_metrics[server]["bandwidth_mbps"] = (
                alpha * bandwidth_mbps + (1 - alpha) * self.server_metrics[server]["bandwidth_mbps"]
            )
            self.server_metrics[server]["success_rate"] = alpha * success + (1 - alpha) * self.server_metrics[server]["success_rate"]

            # Revive others slowly in case they come back online
            for server in self.servers:
                self.server_metrics[server]["success_rate"] = min(1.0, self.server_metrics[server]["success_rate"] + heal_rate)

    def _wget(self, url: str, output_path: str, timeout: Optional[int] = None) -> bool:
        """Download a file from the best server.

        Args:
            url: URL to download from
            output_path: Local path to save the file
        """
        subprocess.run(
            [
                "wget",
                "-q",  # quiet mode
                "-O",
                output_path,  # output file
                "--timeout",
                str(timeout or self.timeout),  # timeout
                url,
            ],
            check=True,
        )

    def _download_file(self, server: str, url_path: str, output_path: Path | str, update_metrics: bool = True) -> bool:
        """Download a file from a specific server.

        Args:
            server: Server URL
            url_path: Path component of the URL
            output_path: Local path to save the file
            update_metrics: Whether to update the server metrics
        """
        # TODO: Make sure we always use Path objects
        output_path = Path(output_path)
        try:
            url = f"{server}/{url_path}"
            temp_path = output_path.with_suffix(".tmp")

            start_time = time.time()
            self._wget(url, temp_path)
            os.rename(temp_path, output_path)

            time_taken = time.time() - start_time
            file_size = output_path.stat().st_size
            bandwidth_mbps = file_size / time_taken / 1e6

            if update_metrics:
                self._update_server_metrics(server, bandwidth_mbps, True)

            logger.debug(f"Downloaded {url_path} from {server} (bandwidth: {bandwidth_mbps:.0f} MB/s)")

            return True

        except Exception as e:
            # Update metrics with failure
            self._update_server_metrics(server, self.timeout, False)
            logger.debug(f"Failed to download {url_path} from {server}: {str(e)}", exc_info=True)

    def download_file(
        self, url_path: str, output_path: str, update_metrics: bool = True, retries: int = RETRY_ATTEMPTS, log_error_on_failure: bool = True
    ) -> bool:
        """Download a file from the best server.

        Args:
            url_path: Path component of the URL (e.g., "v1/shard_001.bin")
            output_path: Local path to save the file
            retries: Number of retries to attempt
            log_error_on_failure: Whether to log an error on failure
        Returns:
            True if successful, False otherwise
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Try downloading from the best servers
        best_servers = self._get_best_servers()

        for retry in range(retries):
            for server in best_servers:
                if self._download_file(server, url_path, output_path, update_metrics):
                    return True

            # If we get here, all servers failed
            if retry < retries - 1:
                # Use fast retries for the first FAST_RETRY_ATTEMPTS attempts, then switch to slow retries, but never stop
                if retry < FAST_RETRY_ATTEMPTS:
                    wait_time = FAST_RETRY_INTERVAL
                    logger.debug(f"Fast retrying download of {url_path} (attempt {retry + 1}/{retries}, wait: {wait_time}s)")
                else:
                    wait_time = SLOW_RETRY_INTERVAL
                    logger.debug(f"Slow retrying download of {url_path} (attempt {retry + 1}/{retries}, wait: {wait_time}s)")

                # Wait before retrying
                time.sleep(wait_time)

        if log_error_on_failure:
            logger.error(f"Failed to download {url_path} after {retries} attempts")
        return False

    def download_distribution_file(self) -> Optional[str]:
        """Download the distribution file.

        Returns:
            Content of the distribution file or None if failed
        """
        temp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp_distribution.txt")

        if self.download_file(DISTRIBUTION_FILE, temp_path, update_metrics=False, log_error_on_failure=False):
            with open(temp_path, "r") as f:
                content = f.read()

            # Clean up
            os.unlink(temp_path)
            return content

        return None

    def download_shards(self, version: str, num_shards: int, output_dir: str) -> List[str]:
        """Download all shards for a version.

        Args:
            version: Version folder name (e.g., "v1")
            num_shards: Number of shards to download
            output_dir: Directory to save the shards

        Returns:
            List of successfully downloaded shard paths
        """
        ensure_dir(output_dir)

        # Track successfully downloaded shards
        successful_shards: List[str] = []
        failed_shards: Set[int] = set()

        # Use a thread pool for concurrent downloads
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_DOWNLOADS) as executor:
            futures = []

            for i in range(num_shards):
                shard_filename = f"shard_{i + 1:05d}.bin"
                url_path = f"{version}/{shard_filename}"
                output_path = os.path.join(output_dir, shard_filename)

                futures.append(executor.submit(self._download_shard_with_retry, url_path, output_path, i))

            # Wait for all downloads to complete
            for i, future in enumerate(futures):
                try:
                    result = future.result()
                    if result:
                        successful_shards.append(result)
                    else:
                        failed_shards.add(i)
                except Exception as e:
                    logger.error(f"Error downloading shard {i + 1}: {str(e)}")
                    failed_shards.add(i)

        # Report summary
        if failed_shards:
            logger.warning(f"Failed to download {len(failed_shards)} out of {num_shards} shards")
            logger.debug(f"Failed shard indices: {sorted(failed_shards)}")
        else:
            logger.info(f"Successfully downloaded all {num_shards} shards")

        return successful_shards

    def _download_shard_with_retry(self, url_path: str, output_path: str, shard_index: int) -> Optional[str]:
        """Download a shard with retries.

        Args:
            url_path: Path component of the URL
            output_path: Local path to save the shard
            shard_index: Index of the shard (for logging)

        Returns:
            Output path if successful, None otherwise
        """
        if self.download_file(url_path, output_path):
            return output_path
        # TODO: This is a hack to try to download the shard again if it fails
        # Should implement a better retry mechanism
        return self._download_shard_with_retry(url_path, output_path, shard_index)
