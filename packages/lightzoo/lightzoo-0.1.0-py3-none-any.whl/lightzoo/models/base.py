# lightzoo/models/base.py

import torch
import torch.nn as nn

class BaseModel(nn.Module):
    """
    BaseModel provides a standard interface for all LightZoo models.
    It can be extended by specific architectures like ResNet, UNet, etc.
    """

    def __init__(self):
        super(BaseModel, self).__init__()

    def forward(self, x):
        raise NotImplementedError("Each model must implement the forward method.")

    def save(self, filepath):
        torch.save(self.state_dict(), filepath)

    def load(self, filepath, map_location=None):
        self.load_state_dict(torch.load(filepath, map_location=map_location))
        self.eval()
