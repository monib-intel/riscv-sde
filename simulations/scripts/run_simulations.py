#!/usr/bin/env python3
"""
Script to run simulations for RISC-V cores.
This script can run simulations for both simple_core and picorv32.
"""

import os
import sys
import argparse
import subprocess
import shutil

def find_workspace_root():
    """Find the workspace root by looking for WORKSPACE.bazel file."""
    current_dir = os.getcwd()
    
    # First check if we're in a Bazel runfiles directory
    if '.runfiles' in current_dir:
        # Extract the workspace root from the runfiles path
        parts = current_dir.split('.runfiles')
        if len(parts) > 1:
            # Get the path before .runfiles
            base_path = parts[0]
            # Try to find the original project path outside of Bazel
            for potential_path in [
                # Standard path
                "/home/monibahmed/exploration/silicon-design-environment",
                # Try to find it in environment variables
                os.environ.get("BUILD_WORKSPACE_DIRECTORY", ""),
                # Get the path before .runfiles, assuming Bazel was invoked from the workspace
                base_path,
            ]:
                if potential_path and os.path.exists(os.path.join(potential_path, 'WORKSPACE.bazel')):
                    return potential_path
    
    # If not in runfiles or couldn't determine, walk up directories looking for WORKSPACE.bazel
    path = current_dir
    while path != '/':
        if os.path.exists(os.path.join(path, 'WORKSPACE.bazel')):
            return path
        path = os.path.dirname(path)
    
    # If we can't find it, use the current directory and print a warning
    print(f"Warning: Could not find workspace root, using current directory: {current_dir}")
    return current_dir

def create_hex_file(output_dir):
    """Create a simple test hex file with a few RISC-V instructions."""
    hex_file = os.path.join(output_dir, "program.hex")
    with open(hex_file, 'w') as f:
        # Write simple test program
        f.write("00000033\n")  # nop
        f.write("00100093\n")  # addi x1, x0, 1
        f.write("00108113\n")  # addi x2, x1, 1
        f.write("00208193\n")  # addi x3, x1, 2
        f.write("00310233\n")  # add x4, x2, x3
    return hex_file

def main():
    parser = argparse.ArgumentParser(description='Run RISC-V core simulations')
    parser.add_argument('--core', choices=['simple_core', 'picorv32'], required=True,
                        help='Which core to simulate')
    parser.add_argument('--hex', type=str, help='Path to hex file to load')
    parser.add_argument('--cycles', type=int, default=10000, 
                        help='Maximum number of simulation cycles')
    args = parser.parse_args()

    # Get project root directory
    project_root = find_workspace_root()
    print(f"Using workspace root: {project_root}")
    
    # Define paths
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    cores_dir = os.path.join(project_root, "design/hardware/rtl/cores")
    testbench = os.path.join(project_root, "design/hardware/rtl/testbench/universal_tb.sv")
    
    # Create hex file for simulation
    if not args.hex:
        hex_file = create_hex_file(output_dir)
        print(f"Created default hex file at {hex_file}")
    else:
        hex_file = args.hex
        if not os.path.isabs(hex_file):
            hex_file = os.path.join(project_root, hex_file)
        print(f"Using provided hex file: {hex_file}")
    
    # Determine core files
    if args.core == 'simple_core':
        core_files = [
            os.path.join(cores_dir, "simple_core/simple_core.v")
        ]
    elif args.core == 'picorv32':
        core_files = [
            os.path.join(cores_dir, "picorv32/picorv32.v"),
            os.path.join(cores_dir, "picorv32/core.v")
        ]
    
    # Run simulation
    print(f"Running simulation for {args.core}...")
    
    # Change to the project root directory to ensure correct path resolution
    original_dir = os.getcwd()
    os.chdir(project_root)
    
    try:
        # Create a simulation directory in output for results
        sim_dir = os.path.join(output_dir, f"{args.core}_sim")
        os.makedirs(sim_dir, exist_ok=True)
        
        # Copy hex file to simulation directory only
        sim_hex_file = os.path.join(sim_dir, "program.hex")
        shutil.copy(hex_file, sim_hex_file)
        print(f"Copied hex file to: {sim_hex_file}")
        
        # Work directly in the simulation directory
        os.chdir(sim_dir)
        
        # Create explicit +hex argument for simulation
        hex_arg = f"+hex={sim_hex_file}"
        
        # Compile with iverilog - put output in the simulation directory
        sim_binary = os.path.join(sim_dir, "sim_core")
        iverilog_cmd = ["iverilog", "-o", sim_binary, "-I", cores_dir, testbench] + core_files
        print(f"Running: {' '.join(iverilog_cmd)}")
        subprocess.run(iverilog_cmd, check=True)
        
        # Run simulation with explicit hex file path
        vvp_cmd = ["vvp", sim_binary, hex_arg]
        print(f"Running: {' '.join(vvp_cmd)}")
        subprocess.run(vvp_cmd, check=True)
        
        # The VCD file is already in the simulation directory since we're working there
        if os.path.exists("sim.vcd"):
            print(f"Simulation waveform generated at {sim_dir}/sim.vcd")
        
        print("Simulation completed successfully!")
    finally:
        # Restore original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    main()
