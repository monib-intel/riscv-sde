#!/usr/bin/env python3
"""
Script to run the full flow for simple_core and hello-world using Bazel
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Run the simple core flow")
    parser.add_argument("--config", default="simple_core_test", help="Configuration file to use")
    parser.add_argument("--flow", default="software,simulation", help="Flow stages to run (comma-separated)")
    args = parser.parse_args()
    
    # Get the project root
    project_root = Path(__file__).parent.parent.parent.absolute()
    
    # Verify config exists
    config_path = project_root / "configs" / f"{args.config}.yaml"
    if not config_path.exists():
        print(f"Error: Configuration file {config_path} not found")
        sys.exit(1)
    
    # Run the software compilation flow
    if "software" in args.flow.split(","):
        print("Running software compilation flow...")
        subprocess.run(
            [sys.executable, "-m", "build.flows.software_flow", "--config", args.config],
            cwd=str(project_root),
            check=True
        )
    
    # Run the simulation flow
    if "simulation" in args.flow.split(","):
        print("Running simulation flow...")
        subprocess.run(
            [sys.executable, "-m", "build.flows.simulation_flow", "--config", args.config],
            cwd=str(project_root),
            check=True
        )
    
    print("Flow completed!")

if __name__ == "__main__":
    main()
