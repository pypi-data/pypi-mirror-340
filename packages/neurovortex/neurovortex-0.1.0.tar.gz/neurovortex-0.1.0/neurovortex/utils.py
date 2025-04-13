import logging
import time
from functools import wraps

def setup_logging(log_file=None):
    """
    Set up logging configuration.
    
    Args:
        log_file (str): Optional file path to save logs to a file.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    if log_file:
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(level=logging.INFO, format=log_format)
    
    return logging.getLogger(__name__)

def timeit(func):
    """
    A decorator to measure the execution time of a function.
    
    Args:
        func (callable): The function to be timed.
    
    Returns:
        callable: Wrapped function with timing.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

def memory_usage():
    """
    Get the current memory usage of the process.
    
    Returns:
        float: Memory usage in MB.
    """
    try:
        import psutil
        process = psutil.Process()
        mem_info = process.memory_info()
        return mem_info.rss / (1024 ** 2)  # Convert bytes to MB
    except ImportError:
        logging.warning("psutil is not installed. Memory usage cannot be determined.")
        return None

def gpu_usage():
    """
    Get the current GPU usage if available.
    
    Returns:
        list: List of tuples containing GPU name and usage percentage.
    """
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        return [(gpu.name, gpu.load * 100) for gpu in gpus]
    except ImportError:
        logging.warning("GPUtil is not installed. GPU usage cannot be determined.")
        return None
