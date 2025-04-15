from setuptools import setup, find_packages

# Read the contents of README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="causaltorch",
    version="0.2.0",
    author="Elija Nzeli",
    author_email="elijahnzeli894@example.com",
    description="A PyTorch library for building generative models with causal constraints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elijahnzeli1/causaltorch",
    project_urls={
        "Bug Tracker": "https://github.com/elijahnzeli1/causaltorch/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "torch>=1.8.0",
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
        "networkx>=2.5",
        "tqdm>=4.61.0",
    ],
    extras_require={
        "text": ["transformers>=4.5.0", "tokenizers>=0.10.2"],
        "image": ["torchvision>=0.9.0", "Pillow>=8.2.0"],
        "video": ["av>=8.0.0", "opencv-python>=4.5.1"],
        "federated": ["pytorch-lightning>=1.3.0"],
        "all": [
            "transformers>=4.5.0",
            "tokenizers>=0.10.2",
            "torchvision>=0.9.0", 
            "Pillow>=8.2.0",
            "av>=8.0.0", 
            "opencv-python>=4.5.1",
            "pytorch-lightning>=1.3.0",
        ],
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "isort>=5.8.0",
            "flake8>=3.9.2",
            "mypy>=0.812",
        ],
    },
)