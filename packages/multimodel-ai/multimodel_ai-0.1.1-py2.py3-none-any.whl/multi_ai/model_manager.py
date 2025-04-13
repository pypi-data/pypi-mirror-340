import torch
import gc
from typing import Dict, Optional, Type
from .models import (
    QwenVLModel,
    QwenAudioModel,
    QwenBaseModel,
    ZonosTTSModel,
    QwenTextModel
)

class ModelManager:
    """Manages multiple AI models with efficient memory handling."""
    
    def __init__(self, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        self.models: Dict[str, QwenBaseModel] = {}
        self.model_classes = {
            "qwen-vl": QwenVLModel,
            "qwen-audio": QwenAudioModel,
            "qwen-text": QwenTextModel,
            "zonos-tts": ZonosTTSModel
        }
        
    def load_model(self, model_name: str, **kwargs) -> QwenBaseModel:
        """
        Load a model, moving other models to CPU if necessary.
        
        Args:
            model_name: Name of the model to load
            **kwargs: Additional arguments for model initialization
            
        Returns:
            The loaded model instance
        """
        if model_name not in self.model_classes:
            raise ValueError(f"Unknown model: {model_name}")
            
        # If model is already loaded, return it
        if model_name in self.models:
            model = self.models[model_name]
            # Only move to device if not using device mapping
            if not getattr(model, 'uses_device_map', False):
                model.to(self.device)
            return model
            
        # Move other models to CPU to free up GPU memory
        self._move_other_models_to_cpu(model_name)
        
        # Create and load new model
        model_class = self.model_classes[model_name]
        model = model_class(**kwargs)
        # Only move to device if not using device mapping
        if not getattr(model, 'uses_device_map', False):
            model.to(self.device)
        self.models[model_name] = model
        
        return model
        
    def unload_model(self, model_name: str):
        """
        Unload a model and free its memory.
        
        Args:
            model_name: Name of the model to unload
        """
        if model_name in self.models:
            model = self.models[model_name]
            # Only move to CPU if not using device mapping
            if not getattr(model, 'uses_device_map', False):
                model.to("cpu")
            del self.models[model_name]
            gc.collect()
            torch.cuda.empty_cache()
            
    def _move_other_models_to_cpu(self, exclude_model: str):
        """Move all models except the specified one to CPU."""
        for name, model in self.models.items():
            if name != exclude_model and not getattr(model, 'uses_device_map', False):
                model.to("cpu")
                
    def get_model(self, model_name: str) -> Optional[QwenBaseModel]:
        """Get a model instance if it exists."""
        return self.models.get(model_name)
        
    def list_loaded_models(self) -> list:
        """Return a list of currently loaded models."""
        return list(self.models.keys())
        
    def clear_all_models(self):
        """Unload all models and free memory."""
        for model_name in list(self.models.keys()):
            self.unload_model(model_name) 