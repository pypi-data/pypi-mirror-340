# lightzoo/utils/load_pretrained.py

import torch
from torchvision import models as tv_models
from transformers import AutoModel, AutoConfig

def load_pretrained_weights(model_name, framework='torchvision', num_classes=1000):
    """
    Load pretrained model weights.
    
    Args:
        model_name (str): Name of the model to load.
        framework (str): 'torchvision' or 'huggingface'.
        num_classes (int): Number of output classes (for reshaping final layer if needed).

    Returns:
        model: A model loaded with pretrained weights.
    """
    if framework == 'torchvision':
        if hasattr(tv_models, model_name):
            model = getattr(tv_models, model_name)(pretrained=True)
            if num_classes != 1000:
                in_features = model.fc.in_features
                model.fc = torch.nn.Linear(in_features, num_classes)
            return model
        else:
            raise ValueError(f"Model {model_name} not found in torchvision.")
    
    elif framework == 'huggingface':
        try:
            config = AutoConfig.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name, config=config)
            return model
        except Exception as e:
            raise ValueError(f"Failed to load model from HuggingFace: {e}")
    
    else:
        raise ValueError("Framework must be either 'torchvision' or 'huggingface'")
