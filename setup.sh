#!/bin/bash
# setup.sh - Sets up the development environment for the silicon design environment

set -e  # Exit on error

echo "=== Setting up Silicon Design Environment ==="

# Create a new virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv .venv
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source .venv/bin/activate

# Install all dependencies (including dev dependencies)
echo "Installing dependencies..."
uv pip install -e ".[dev]"

# Verify the installation
echo "Verifying installation..."
python -c "import sys; print(f'Python {sys.version} installed successfully.')"
python -m pytest tests/test_dependencies.py -v

echo "=== Setup Complete ==="
echo "To activate the virtual environment, run:"
echo "source .venv/bin/activate"
