# setup.py

from setuptools import setup, find_packages

setup(
    name="lightzoo",
    version="0.1.0",
    description="A lightweight model zoo for quick prototyping and experimentation.",
    author="Harich Selva M C",
    author_email="harichselvamc@gmail.com",
    url="https://github.com/harichselvamc/lightzoo",
    packages=find_packages(),
    install_requires=[
        "torch>=1.10",
        "torchvision>=0.11",
        "transformers>=4.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
