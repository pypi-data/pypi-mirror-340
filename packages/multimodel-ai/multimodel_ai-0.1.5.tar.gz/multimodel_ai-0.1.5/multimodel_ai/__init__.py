"""
MultiModel-AI - A Python module for efficient multi-model AI inference with memory management
"""

from .model_manager import ModelManager
from .models import (
    QwenVLModel,
    QwenCoderModel,
    QwenBaseModel,
    QwenAudioModel,
    ZonosTTSModel,
    QwenTextModel
)

__version__ = "0.1.0"

__all__ = [
    'ModelManager',
    'QwenVLModel',
    'QwenCoderModel',
    'QwenBaseModel',
    'QwenAudioModel',
    'ZonosTTSModel',
    'QwenTextModel'
] 