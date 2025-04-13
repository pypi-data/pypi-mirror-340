import os
import shutil
import subprocess
import sys
from setuptools import setup, find_namespace_packages
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Install the zonos wheel file
        wheel_path = os.path.join(os.path.dirname(__file__), 'multimodel_ai', 'data', 'zonos-0.1.0-py3-none-any.whl')
        if os.path.exists(wheel_path):
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-deps', wheel_path])
            except subprocess.CalledProcessError as e:
                print(f"Warning: Failed to install zonos wheel: {e}")
        else:
            print("Warning: zonos wheel file not found at", wheel_path)

# Create a data directory in the package
data_dir = os.path.join(os.path.dirname(__file__), 'multimodel_ai', 'data')
os.makedirs(data_dir, exist_ok=True)

setup(
    name="multimodel-ai",
    version="0.1.3",
    packages=find_namespace_packages(include=['multimodel_ai', 'multimodel_ai.*']),
    include_package_data=True,
    install_requires=[
        "accelerate>=1.6.0",
        "qwen-omni-utils[decord]>=0.0.4",
        "qwen-vl-utils[decord]==0.0.8",
        "torchvision>=0.21.0",
        "bitsandbytes>=0.45.5",
        "transformers>=4.37.0",
        "torch>=2.6.0",
        "torchaudio>=2.6.0",
        "librosa>=0.11.0",
        "soundfile>=0.13.1",
        "numpy>=1.22.3",
        "scipy>=1.6.0",
    ],
    package_data={
        'multimodel_ai.data': ['*.whl'],
    },
    setup_requires=["wheel"],
    cmdclass={
        'install': PostInstallCommand,
    },
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
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
) 