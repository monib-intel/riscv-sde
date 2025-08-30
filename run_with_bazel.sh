#!/bin/bash
# Wrapper script to run simulations with Bazel and Prefect orchestration

# Check if bazel is installed
if ! command -v bazel &> /dev/null; then
    echo "Error: bazel is not installed. Please install bazel first."
    exit 1
fi

# Display help information if requested
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --core=CORE                 The core to simulate (simple_core, picorv32)"
    echo "  --clean                     Clean build artifacts before running"
    echo "  --output-dir=DIR            Directory to store outputs (default: output)"
    echo "  --config=FILE               Configuration file to use"
    echo "  --build-docs                Build documentation"
    echo "  --flows=FLOWS               Comma-separated list of flows to run"
    echo "  --working-dir=DIR           Working directory for Bazel commands"
    echo ""
    exit 0
fi

# Run the orchestration flow using bazel
bazel run //:orchestration -- "$@"
