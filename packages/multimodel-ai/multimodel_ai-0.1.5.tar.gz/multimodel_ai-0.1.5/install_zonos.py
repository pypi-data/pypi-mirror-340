#!/usr/bin/env python
"""
Script to install the zonos package from the local wheel file.
This script should be run before installing the multimodel-ai package.
"""

import os
import subprocess
import sys

def install_zonos():
    """Install the zonos package from the local wheel file."""
    # Get the path to the zonos wheel file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zonos_wheel = os.path.join(os.path.dirname(script_dir), 'Zonos', 'zonos-0.1.0-py3-none-any.whl')
    
    if not os.path.exists(zonos_wheel):
        print(f"Error: Could not find zonos wheel file at {zonos_wheel}")
        sys.exit(1)
    
    print(f"Installing zonos from {zonos_wheel}...")
    
    # Uninstall any existing zonos package
    subprocess.check_call([
        sys.executable,
        '-m',
        'pip',
        'uninstall',
        '-y',
        'zonos'
    ])
    
    # Install the zonos wheel
    subprocess.check_call([
        sys.executable,
        '-m',
        'pip',
        'install',
        '--no-cache-dir',
        zonos_wheel
    ])
    
    print("Successfully installed zonos from local wheel")

if __name__ == '__main__':
    install_zonos() 