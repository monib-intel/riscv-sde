#!/bin/bash
# Script to build the documentation

# Exit on error
set -e

# Change to the docs directory
cd "$(dirname "$0")"

# Install dependencies if needed
if [ "$1" == "--install" ]; then
    echo "Installing documentation dependencies..."
    pip install -e "..[docs]"
fi

# Build the documentation
echo "Building HTML documentation..."
make clean html

# Check if build was successful
if [ -d "_build/html" ]; then
    echo "Documentation built successfully in _build/html/"
    echo "To view the documentation, open _build/html/index.html in your browser"
else
    echo "Error: Documentation build failed"
    exit 1
fi

# Optionally open the documentation
if [ "$1" == "--open" ] || [ "$2" == "--open" ]; then
    echo "Opening documentation in browser..."
    if command -v xdg-open > /dev/null; then
        xdg-open _build/html/index.html
    elif command -v open > /dev/null; then
        open _build/html/index.html
    else
        echo "Cannot open browser automatically. Please open _build/html/index.html manually."
    fi
fi
