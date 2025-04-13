# Import core components
from .optimizer import AIOptimizer
from .model_loader import detect_model_format, load_model, save_model
from .resource_manager import ResourceManager
from .utils import setup_logging, timeit, memory_usage, gpu_usage

# Define the public API for the package
__all__ = [
    "AIOptimizer",
    "detect_model_format",
    "load_model",
    "save_model",
    "ResourceManager",
    "setup_logging",
    "timeit",
    "memory_usage",
    "gpu_usage",
]

# Package metadata
__version__ = "0.1.0"
__author__ = "Boring-Dude"
__email__ = "cybergx932@gmail.com"
__description__ = "An AI Optimizer module for improving performance."
__url__ = "https://github.com/Boring-Dude/neurovortex"

# Initialize logging
logger = setup_logging()
logger.info(f"Initialized NeuroVortex package (version {__version__})")
