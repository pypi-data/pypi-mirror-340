import os
import shutil
from setuptools import setup, find_packages

# Create a data directory in the package
data_dir = os.path.join(os.path.dirname(__file__), 'multimodel_ai', 'data')
os.makedirs(data_dir, exist_ok=True)

setup(
    name="multimodel-ai",
    version="0.1.2",
    packages=find_packages(),
    package_data={
        'multimodel_ai': ['data/*.whl'],
    },
    install_requires=[
        "accelerate>=1.6.0",
        "qwen-omni-utils[decord]>=0.0.4",
        "qwen-vl-utils[decord]==0.0.8",
        "torchvision>=0.21.0",
        "bitsandbytes>=0.45.5",
        "transformers>=4.37.0",
    ],
    options={
        "bdist_wheel": {
            "universal": True
        }
    },
    setup_requires=["wheel"],
    entry_points={
        "console_scripts": [
            "multimodel-ai=multimodel_ai.cli:main",
        ],
    },
    python_requires=">=3.8",
    author="VRImage",
    author_email="vrimage70@gmail.com",
    description="A Python module for efficient multi-model AI inference with memory management",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/VRImage/multimodel-ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
) 