#!/bin/bash

# Stage 0: Environment and Infrastructure Verification
# This script runs the dependency tests using the existing environment

set -e  # Exit on any error

echo "🔧 Stage 0: Environment and Infrastructure Verification"
echo "================================================="

# Check if we're running in Bazel sandbox (readonly filesystem)
if [[ "$TEST_TMPDIR" != "" ]]; then
    echo "✅ Bazel test environment detected"
    echo "Using system Python with minimal dependency check..."
    
    # In Bazel sandbox, just run basic Python checks without uv
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "❌ No Python found in Bazel sandbox"
        exit 1
    fi
    
    # Set a temporary UV cache in the test temp directory to avoid readonly errors
    export UV_CACHE_DIR="$TEST_TMPDIR/uv_cache"
    mkdir -p "$UV_CACHE_DIR"
    
elif [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
    PYTHON_CMD="python"
elif command -v uv &> /dev/null; then
    echo "✅ UV detected, running with uv"
    PYTHON_CMD="uv run python"
else
    echo "❌ No virtual environment active and uv not found"
    echo "Please activate your virtual environment or install uv"
    exit 1
fi

# Run the dependency tests
echo ""
echo "Running dependency verification tests..."
$PYTHON_CMD tests/test_dependencies.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Stage 0: Environment verification completed successfully!"
    echo "Your development environment is ready for the PPA study."
    exit 0
else
    echo ""
    echo "❌ Stage 0: Environment verification failed!"
    echo "Please fix the issues above before proceeding."
    exit 1
fi