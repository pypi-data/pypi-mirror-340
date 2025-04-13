import os
from setuptools import setup, find_packages
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Run the transformers installation script
        import multi_ai.post_install
        multi_ai.post_install.install_transformers()

setup(
    name="multimodel-ai",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "accelerate",
        "qwen-omni-utils[decord]",
        "qwen-vl-utils[decord]==0.0.8",
        "torchvision",
        "bitsandbytes",
        "zonos",
    ],
    options={
        "bdist_wheel": {
            "universal": True
        }
    },
    setup_requires=["wheel"],
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        "console_scripts": [
            "multi-ai=multi_ai.cli:main",
        ],
    },
    python_requires=">=3.8",
    author="VRImage",
    author_email="vrimage70@gmail.com",
    description="A Python module for efficient multi-model AI inference with memory management",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/VRImage/multi-ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 