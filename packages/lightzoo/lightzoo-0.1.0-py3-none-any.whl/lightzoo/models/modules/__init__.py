# lightzoo/models/modules/__init__.py

"""
Swappable custom modules for LightZoo models.
Includes attention mechanisms, convolution blocks, etc.
"""

from .attention.py import MultiHeadSelfAttention
from .convolutions import DepthwiseSeparableConv

__all__ = [
    "MultiHeadSelfAttention",
    "DepthwiseSeparableConv"
]
