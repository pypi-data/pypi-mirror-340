# tests/test_utils.py

import pytest
from lightzoo.utils import load_pretrained_weights

def test_torchvision_model_load():
    model = load_pretrained_weights("resnet18", framework="torchvision", num_classes=1000)
    assert model is not None
    assert hasattr(model, "forward"), "Loaded model does not have a forward method."

def test_invalid_model_name():
    with pytest.raises(ValueError):
        load_pretrained_weights("nonexistent_model", framework="torchvision")

def test_invalid_framework():
    with pytest.raises(ValueError):
        load_pretrained_weights("resnet18", framework="unsupported_framework")
