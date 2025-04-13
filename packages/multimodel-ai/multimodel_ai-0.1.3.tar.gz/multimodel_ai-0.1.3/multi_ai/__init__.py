"""
MultiModel-AI: A framework for managing and running multiple AI models.
"""

from .models import ModelManager
from .utils import (
    load_model_config,
    save_model_config,
    get_device,
    set_seed
)

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    'ModelManager',
    'load_model_config',
    'save_model_config',
    'get_device',
    'set_seed'
] 