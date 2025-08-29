#!/usr/bin/env python3
"""
Wrapper script to run simulations with different cores.
This script provides a user-friendly interface to the Bazel targets.
"""

import argparse
import subprocess
import sys
import os
import shutil

def main():
    """Main function to parse arguments and run simulations."""
    parser = argparse.ArgumentParser(description='Run RISC-V core simulations')
    parser.add_argument('--core', choices=['simple_core', 'picorv32'], 
                        default='simple_core',
                        help='The core to simulate (default: simple_core)')
    parser.add_argument('--clean', action='store_true',
                        help='Clean build artifacts before running')
    parser.add_argument('--output-dir', default='output',
                        help='Directory to store simulation outputs (default: output)')
    parser.add_argument('--config', default='build/configs/simple_core_test.yaml',
                        help='Configuration file to use (default: build/configs/simple_core_test.yaml)')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(f"{args.output_dir}/{args.core}_sim", exist_ok=True)
    
    # Clean if requested
    if args.clean:
        print("Cleaning previous build artifacts...")
        subprocess.run(["bazel", "clean"], check=True)
        
        # Also clean generated files from output directory
        print(f"Cleaning generated files from {args.output_dir}/{args.core}_sim...")
        for f in ['program.hex', 'sim_core', 'sim.vcd']:
            if os.path.exists(f"{args.output_dir}/{args.core}_sim/{f}"):
                os.remove(f"{args.output_dir}/{args.core}_sim/{f}")
    
    # Run the appropriate simulation with output redirection
    if args.core == 'simple_core':
        print(f"Running simulation for simple_core...")
        os.environ["OUTPUT_DIR"] = f"{args.output_dir}/{args.core}_sim"
        os.environ["CONFIG_FILE"] = args.config
        subprocess.run(["bazel", "run", "//simulations:simple_core_simulation"], check=True)
    else:
        print(f"Running simulation for picorv32...")
        os.environ["OUTPUT_DIR"] = f"{args.output_dir}/{args.core}_sim"
        os.environ["CONFIG_FILE"] = args.config
        subprocess.run(["bazel", "run", "//simulations:picorv32_simulation"], check=True)
    
    # Clean up any generated files in the root directory
    for f in ['program.hex', 'sim_core', 'sim.vcd']:
        if os.path.exists(f):
            dest = f"{args.output_dir}/{args.core}_sim/{f}"
            print(f"Moving {f} to {dest}")
            shutil.move(f, dest)
    
    print(f"Simulation complete. Results are in the {args.output_dir}/{args.core}_sim directory.")

if __name__ == "__main__":
    main()
