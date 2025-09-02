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

# Set default flows to just software if not specified
# This avoids trying to run simulation and analysis flows that might not be fully implemented
DEFAULT_FLOWS="--flows=software"

# Check if flows are specified in the arguments
if [[ ! "$*" =~ --flows ]]; then
    echo "No flows specified, defaulting to software flow only"
    SET_DEFAULT_FLOWS="$DEFAULT_FLOWS"
else
    SET_DEFAULT_FLOWS=""
fi

# Run the orchestration flow using bazel
# Add working directory explicitly if not provided
if [[ ! "$*" =~ --working-dir ]]; then
    WORKING_DIR="$(pwd)"
    bazel run //:orchestration -- --working-dir="$WORKING_DIR" $SET_DEFAULT_FLOWS "$@"
else
    bazel run //:orchestration -- $SET_DEFAULT_FLOWS "$@"
fi
