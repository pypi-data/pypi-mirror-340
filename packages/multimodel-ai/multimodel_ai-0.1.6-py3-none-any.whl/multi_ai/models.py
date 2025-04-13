"""
Core model management functionality for MultiModel-AI.
"""

import logging
from typing import Any, Dict, List, Optional, Union

import torch
from torch import nn

from .utils import get_device, load_model_config, save_model_config, set_seed

logger = logging.getLogger(__name__)

class ModelManager:
    """
    A class to manage multiple AI models and their interactions.
    
    This class handles loading, unloading, and running inference with multiple models,
    managing their resources and configurations.
    """
    
    def __init__(self, config_path: Optional[str] = None, seed: Optional[int] = None):
        """
        Initialize the ModelManager.
        
        Args:
            config_path: Optional path to a configuration file
            seed: Optional random seed for reproducibility
        """
        self.models: Dict[str, nn.Module] = {}
        self.configs: Dict[str, Dict[str, Any]] = {}
        self.device = get_device()
        
        if seed is not None:
            set_seed(seed)
            
        if config_path:
            self.load_config(config_path)
            
    def load_model(self, name: str, model: nn.Module, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Load a model into the manager.
        
        Args:
            name: Unique identifier for the model
            model: The PyTorch model to load
            config: Optional configuration dictionary for the model
        """
        if name in self.models:
            logger.warning(f"Model {name} already exists. Unloading previous version.")
            self.unload_model(name)
            
        self.models[name] = model.to(self.device)
        if config:
            self.configs[name] = config
            
        logger.info(f"Loaded model {name}")
        
    def unload_model(self, name: str) -> None:
        """
        Unload a model from the manager.
        
        Args:
            name: Name of the model to unload
        """
        if name in self.models:
            del self.models[name]
            if name in self.configs:
                del self.configs[name]
            logger.info(f"Unloaded model {name}")
        else:
            logger.warning(f"Model {name} not found")
            
    def get_model(self, name: str) -> Optional[nn.Module]:
        """
        Get a loaded model by name.
        
        Args:
            name: Name of the model to retrieve
            
        Returns:
            The model if found, None otherwise
        """
        return self.models.get(name)
        
    def load_config(self, config_path: str) -> None:
        """
        Load configuration from a file.
        
        Args:
            config_path: Path to the configuration file
        """
        config = load_model_config(config_path)
        for name, model_config in config.get('models', {}).items():
            self.configs[name] = model_config
            
    def save_config(self, config_path: str) -> None:
        """
        Save current configuration to a file.
        
        Args:
            config_path: Path where to save the configuration
        """
        config = {'models': self.configs}
        save_model_config(config, config_path)
        
    def run_inference(self, model_name: str, inputs: Any) -> Any:
        """
        Run inference with a specific model.
        
        Args:
            model_name: Name of the model to use
            inputs: Input data for the model
            
        Returns:
            Model outputs
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
            
        model = self.models[model_name]
        model.eval()
        
        with torch.no_grad():
            if isinstance(inputs, torch.Tensor):
                inputs = inputs.to(self.device)
            outputs = model(inputs)
            
        return outputs 