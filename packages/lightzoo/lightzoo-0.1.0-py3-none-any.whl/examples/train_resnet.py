# examples/train_resnet.py

import torch
import torch.nn as nn
import torch.optim as optim
from lightzoo.models import ResNet
from lightzoo.datasets import get_dataloader

def train_resnet():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load model
    model = ResNet(num_classes=10).to(device)

    # Dataloaders
    train_loader = get_dataloader("CIFAR10", batch_size=64, train=True)
    test_loader = get_dataloader("CIFAR10", batch_size=64, train=False)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    for epoch in range(5):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch {epoch+1}, Loss: {running_loss / len(train_loader):.4f}")

    print("✅ Training complete.")

if __name__ == "__main__":
    train_resnet()
