from setuptools import setup

setup(
    # All configuration is now in pyproject.toml
    # This file is kept minimal for backward compatibility
    packages=['multi_ai'],
    package_data={
        'multi_ai': ['*.json', '*.txt', '*.md'],
    },
    include_package_data=True,
) 