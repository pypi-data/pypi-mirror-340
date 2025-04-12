# tests/test_models.py

import torch
import pytest
from lightzoo.models import ResNet, UNet, Transformer

def test_resnet_output_shape():
    model = ResNet(num_classes=10)
    x = torch.randn(4, 3, 32, 32)  # batch of 4 RGB images
    out = model(x)
    assert out.shape == (4, 10), f"Expected (4, 10), got {out.shape}"

def test_unet_output_shape():
    model = UNet(in_channels=3, out_channels=1)
    x = torch.randn(2, 3, 128, 128)  # batch of 2 RGB images
    out = model(x)
    assert out.shape == (2, 1, 128, 128), f"Expected (2, 1, 128, 128), got {out.shape}"

def test_transformer_output_shape():
    model = Transformer(input_dim=512, num_tokens=10000, max_len=128, num_classes=5)
    x = torch.randint(0, 10000, (2, 128))  # batch of 2 token sequences
    out = model(x)
    assert out.shape == (2, 5), f"Expected (2, 5), got {out.shape}"
