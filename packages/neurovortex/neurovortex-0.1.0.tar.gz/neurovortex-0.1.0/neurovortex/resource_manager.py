import psutil
import logging

class ResourceManager:
    """
    A class to monitor and manage system resources.
    """

    @staticmethod
    def get_cpu_usage(interval=1):
        """
        Get the current CPU usage percentage.

        Args:
            interval (int): Interval in seconds to calculate CPU usage.

        Returns:
            float: CPU usage percentage.
        """
        return psutil.cpu_percent(interval=interval)

    @staticmethod
    def get_memory_usage():
        """
        Get the current memory usage.

        Returns:
            dict: Memory usage statistics (total, available, used, percent).
        """
        memory = psutil.virtual_memory()
        return {
            "total": memory.total / (1024 ** 3),  # Convert to GB
            "available": memory.available / (1024 ** 3),  # Convert to GB
            "used": memory.used / (1024 ** 3),  # Convert to GB
            "percent": memory.percent,
        }

    @staticmethod
    def get_gpu_usage():
        """
        Get the current GPU usage (if applicable).

        Returns:
            list: List of tuples containing GPU name and usage percentage.
        """
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            return [
                {
                    "name": gpu.name,
                    "load": gpu.load * 100,
                    "memory_used": gpu.memoryUsed,
                    "memory_total": gpu.memoryTotal,
                    "temperature": gpu.temperature,
                }
                for gpu in gpus
            ]
        except ImportError:
            logging.warning("GPUtil is not installed. GPU usage cannot be determined.")
            return None

    @staticmethod
    def get_disk_usage(path="/"):
        """
        Get the current disk usage for a given path.

        Args:
            path (str): Path to check disk usage (default is root directory).

        Returns:
            dict: Disk usage statistics (total, used, free, percent).
        """
        disk = psutil.disk_usage(path)
        return {
            "total": disk.total / (1024 ** 3),  # Convert to GB
            "used": disk.used / (1024 ** 3),  # Convert to GB
            "free": disk.free / (1024 ** 3),  # Convert to GB
            "percent": disk.percent,
        }

    @staticmethod
    def get_network_stats():
        """
        Get the current network I/O statistics.

        Returns:
            dict: Network I/O statistics (bytes sent, bytes received).
        """
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent / (1024 ** 2),  # Convert to MB
            "bytes_received": net_io.bytes_recv / (1024 ** 2),  # Convert to MB
        }

    @staticmethod
    def log_system_stats():
        """
        Log the current system resource statistics.
        """
        logging.info("CPU Usage: %.2f%%", ResourceManager.get_cpu_usage())
        memory = ResourceManager.get_memory_usage()
        logging.info(
            "Memory Usage: %.2f%% (Used: %.2f GB / Total: %.2f GB)",
            memory["percent"],
            memory["used"],
            memory["total"],
        )
        disk = ResourceManager.get_disk_usage()
        logging.info(
            "Disk Usage: %.2f%% (Used: %.2f GB / Total: %.2f GB)",
            disk["percent"],
            disk["used"],
            disk["total"],
        )
        network = ResourceManager.get_network_stats()
        logging.info(
            "Network I/O: Sent: %.2f MB, Received: %.2f MB",
            network["bytes_sent"],
            network["bytes_received"],
        )
        gpu_stats = ResourceManager.get_gpu_usage()
        if gpu_stats:
            for gpu in gpu_stats:
                logging.info(
                    "GPU: %s, Load: %.2f%%, Memory Used: %.2f MB / %.2f MB, Temp: %.2f°C",
                    gpu["name"],
                    gpu["load"],
                    gpu["memory_used"],
                    gpu["memory_total"],
                    gpu["temperature"],
                )
