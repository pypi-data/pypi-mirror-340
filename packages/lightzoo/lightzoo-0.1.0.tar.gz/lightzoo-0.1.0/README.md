# 🦓 LightZoo

**LightZoo** is a lightweight model zoo for fast experimentation and prototyping.  
It includes clean, minimal implementations of popular architectures like **ResNet**, **U-Net**, and **Transformer**, along with swappable modules for easy customization.

---

## ✨ Features
- ✅ Minimal, readable code for key architectures
- 🔄 Easily swappable modules (attention layers, conv blocks)
- 🤖 Pretrained model loading (HuggingFace, Torchvision)
- 🧪 Testable and modular structure
- 🚀 Ready-to-run examples and training scripts

---

## 🛠️ Installation
```bash
git clone https://github.com/harichselvamc/lightzoo.git
cd lightzoo
pip install -e .
```

## 🚀 Quick Start

### Example: Train ResNet on CIFAR-10
```bash
python examples/train_resnet.py
```

Or use models directly in your scripts:
```python
from lightzoo.models import ResNet
model = ResNet(num_classes=10)
```

## 📦 Models Included

| Model | Purpose |
|-------|---------|
| ResNet | Image classification |
| UNet | Semantic segmentation |
| Transformer | Sequence modeling |

## 🔁 Pretrained Model Loader

Supports:
- torchvision.models
- transformers (HuggingFace)

```python
from lightzoo.utils import load_pretrained_weights
model = load_pretrained_weights("resnet18", framework="torchvision", num_classes=10)
```

## 🗂️ Project Structure

```
lightzoo/
│
├── models/             # ResNet, UNet, Transformer
│   └── modules/        # Custom layers like attention, conv
├── utils/              # Pretrained model loader
├── datasets/           # Built-in dataset loader
├── examples/           # Sample training scripts
├── tests/              # Unit tests
├── setup.py            # Install config
├── README.md           # Project description
└── requirements.txt    # Dependencies
```

## ✅ Requirements

- Python 3.7+
- PyTorch >= 1.10
- torchvision >= 0.11
- transformers >= 4.0

Install dependencies with:
```bash
pip install -r requirements.txt
```

## 🧪 Run Tests
```bash
pytest tests/
```