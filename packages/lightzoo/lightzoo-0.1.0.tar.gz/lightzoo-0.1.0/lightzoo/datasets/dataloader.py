# lightzoo/datasets/dataloader.py

import torch
from torchvision import datasets, transforms

def get_dataloader(dataset_name="CIFAR10", data_dir="./data", batch_size=32, train=True, download=True):
    """
    Returns a DataLoader for a standard dataset.
    
    Args:
        dataset_name (str): Name of the dataset (CIFAR10, MNIST, etc.)
        data_dir (str): Directory to store/download the data.
        batch_size (int): Number of samples per batch.
        train (bool): Whether to load the training or test set.
        download (bool): Whether to download the dataset if not present.

    Returns:
        torch.utils.data.DataLoader: DataLoader object
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)) if dataset_name == "MNIST" else transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    if dataset_name.upper() == "CIFAR10":
        dataset = datasets.CIFAR10(root=data_dir, train=train, download=download, transform=transform)
    elif dataset_name.upper() == "MNIST":
        dataset = datasets.MNIST(root=data_dir, train=train, download=download, transform=transform)
    else:
        raise ValueError(f"Dataset '{dataset_name}' not supported.")

    return torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=train)
