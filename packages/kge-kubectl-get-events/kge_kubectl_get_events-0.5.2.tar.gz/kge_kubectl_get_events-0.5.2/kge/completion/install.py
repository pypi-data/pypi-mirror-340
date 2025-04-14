#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

def install_completions():
    """Install shell completions for kge."""
    # Get the user's home directory
    home = Path.home()
    
    # Install zsh completion
    zsh_completion_dir = home / ".zsh" / "completion"
    zsh_completion_dir.mkdir(parents=True, exist_ok=True)
    
    # Get the path to the completion file in the package
    package_dir = Path(__file__).parent
    completion_file = package_dir / "_kge"
    
    # Copy the completion file
    shutil.copy2(completion_file, zsh_completion_dir)
    
    # Add the completion directory to fpath if not already present
    zshrc = home / ".zshrc"
    if zshrc.exists():
        with open(zshrc, 'r') as f:
            content = f.read()
        
        fpath_line = f'fpath=($fpath {zsh_completion_dir})'
        if fpath_line not in content:
            with open(zshrc, 'a') as f:
                f.write(f'\n# Added by kge\n{fpath_line}\n')
    
    print(f"Shell completions installed successfully!")
    print(f"Please restart your shell or run 'source ~/.zshrc' to enable completions.")

if __name__ == "__main__":
    install_completions() 