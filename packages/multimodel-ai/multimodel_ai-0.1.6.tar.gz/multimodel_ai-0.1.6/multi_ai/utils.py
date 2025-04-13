"""
Utility functions for MultiModel-AI.
"""

import json
import logging
import os
import random
from typing import Any, Dict, Optional

import numpy as np
import torch

logger = logging.getLogger(__name__)

def get_device() -> torch.device:
    """
    Get the appropriate device for model inference.
    
    Returns:
        torch.device: The device to use (CUDA if available, CPU otherwise)
    """
    if torch.cuda.is_available():
        return torch.device('cuda')
    return torch.device('cpu')

def set_seed(seed: int) -> None:
    """
    Set random seeds for reproducibility.
    
    Args:
        seed: The random seed to use
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

def load_model_config(config_path: str) -> Dict[str, Any]:
    """
    Load model configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dict containing the configuration
        
    Raises:
        FileNotFoundError: If the config file doesn't exist
        json.JSONDecodeError: If the config file is not valid JSON
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        logger.info(f"Loaded configuration from {config_path}")
        return config
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing configuration file: {e}")
        raise

def save_model_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Save model configuration to a JSON file.
    
    Args:
        config: Configuration dictionary to save
        config_path: Path where to save the configuration
    """
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        logger.info(f"Saved configuration to {config_path}")
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        raise 