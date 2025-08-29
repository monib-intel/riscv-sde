#!/usr/bin/env python3
"""
Setup script for the Silicon Design Environment.
Replaces setup.sh with a pure Python implementation.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and handle errors."""
    if description:
        print(f"🔧 {description}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_uv_available():
    """Check if uv is available."""
    return shutil.which("uv") is not None

def main():
    print("=== Setting up Silicon Design Environment ===")
    
    # When running from Bazel, we need to find the actual project root
    # The runfiles directory structure is different from source
    current_dir = Path(__file__).parent
    if 'bazel-out' in str(current_dir):
        # Running from Bazel - find the actual project root
        # Look for common project markers
        project_root = Path.cwd()
        while project_root != project_root.parent:
            if (project_root / 'pyproject.toml').exists():
                break
            project_root = project_root.parent
        else:
            # Fallback to current working directory
            project_root = Path.cwd()
    else:
        # Running directly - use script location
        project_root = current_dir.parent
    
    os.chdir(project_root)
    print(f"Working in: {project_root}")
    
    if not check_uv_available():
        print("❌ Error: 'uv' package manager is not installed.")
        print("Please install uv first: https://docs.astral.sh/uv/getting-started/installation/")
        return 1
    
    # Create virtual environment if it doesn't exist
    venv_path = project_root / ".venv"
    if not venv_path.exists():
        if not run_command("uv venv .venv", "Creating virtual environment..."):
            return 1
    else:
        print("✅ Virtual environment already exists.")
    
    # Install dependencies
    print("📦 Installing Python dependencies...")
    
    # Try installing basic dependencies first
    basic_deps = ["pytest", "tomli", "numpy", "pandas", "matplotlib", "pyyaml"]
    deps_str = ' '.join(basic_deps)
    if not run_command(f"uv pip install {deps_str}", "Installing basic dependencies..."):
        print("⚠️  Warning: Some dependencies may have failed to install")
        # Continue anyway
    
    # Verify installation by running dependency tests
    print("🔍 Verifying installation...")
    if not run_command("uv run python tests/test_dependencies.py", "Running dependency verification..."):
        print("❌ Setup verification failed!")
        return 1
    
    print("✅ === Setup Complete ===")
    print("Environment is ready! You can now run:")
    print("  bazel test //:verify_environment  # Verify environment")
    print("  bazel test //flows:all_flow_files  # Test flow files")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())