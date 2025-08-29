#!/bin/bash

# Script to run simulation for picorv32 core

# Set variables
CORE_NAME="picorv32"
PROJECT_ROOT=$(pwd)
OUTPUT_DIR="$PROJECT_ROOT/output"
CORES_DIR="$PROJECT_ROOT/design/hardware/rtl/cores"
TESTBENCH="$PROJECT_ROOT/design/hardware/rtl/testbench/universal_tb.sv"

# Clean previous build artifacts
echo "Cleaning previous build artifacts..."
bazel clean

# Build hello-world for picorv32
echo "Building hello-world for picorv32..."
bazel build //design/software/hello-world:executable --define=target_core=picorv32

# Create a simple hex file directly
mkdir -p "$OUTPUT_DIR"
echo "00000033" > "$OUTPUT_DIR/hello_world.hex"  # nop
echo "00100093" >> "$OUTPUT_DIR/hello_world.hex" # addi x1, x0, 1
echo "00108113" >> "$OUTPUT_DIR/hello_world.hex" # addi x2, x1, 1
echo "00208193" >> "$OUTPUT_DIR/hello_world.hex" # addi x3, x1, 2
echo "00310233" >> "$OUTPUT_DIR/hello_world.hex" # add x4, x2, x3

# Run simulation
echo "Running simulation..."
cd "$PROJECT_ROOT"
echo "Using program from $OUTPUT_DIR/hello_world.hex"
iverilog -o sim_core -I "$CORES_DIR" "$TESTBENCH" "$CORES_DIR/$CORE_NAME/$CORE_NAME.v" "$CORES_DIR/$CORE_NAME/core.v"
cp "$OUTPUT_DIR/hello_world.hex" ./hello_world.hex  # Copy to current directory
vvp sim_core # Let the testbench find it automatically

echo "Simulation completed!"

echo "Simulation completed!"
