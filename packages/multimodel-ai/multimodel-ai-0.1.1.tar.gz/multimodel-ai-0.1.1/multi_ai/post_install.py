"""Post-installation script to install the correct version of transformers."""
import subprocess
import sys

def install_transformers():
    """Install the correct version of transformers from GitHub."""
    try:
        # First uninstall any existing transformers
        subprocess.check_call([
            sys.executable,
            '-m',
            'pip',
            'uninstall',
            '-y',
            'transformers'
        ])
        
        # Install the specific version from GitHub
        subprocess.check_call([
            sys.executable,
            '-m',
            'pip',
            'install',
            'git+https://github.com/huggingface/transformers'
        ])
        
        print("Successfully installed transformers from GitHub")
    except subprocess.CalledProcessError as e:
        print(f"Error installing transformers: {e}")
        raise

if __name__ == '__main__':
    install_transformers() 