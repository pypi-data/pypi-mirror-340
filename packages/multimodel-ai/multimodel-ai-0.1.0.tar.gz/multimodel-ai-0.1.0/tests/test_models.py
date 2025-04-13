"""Test the models module."""
import pytest
from multi_ai import ModelManager

def test_model_manager_initialization():
    """Test that the ModelManager can be initialized."""
    manager = ModelManager()
    assert manager is not None
    assert manager.device in ["cuda", "cpu"]

def test_model_loading():
    """Test that models can be loaded."""
    manager = ModelManager()
    try:
        model = manager.load_model("qwen-text")
        assert model is not None
    finally:
        manager.clear_all_models() 