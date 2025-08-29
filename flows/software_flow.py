#!/usr/bin/env python3
"""
Software Compilation Flow

This script handles the compilation of software benchmarks for various RISC-V cores,
producing binaries and executable files for simulation and analysis.
"""

import os
import sys
from prefect import task, Flow
from prefect.engine.results import LocalResult

# Import utilities
from flows.utils.config import get_software_config
from flows.utils.bazel import bazel_build

@task
def compile_software(study_params):
    """
    Compile software benchmarks for the specified configurations.
    
    Args:
        study_params: Dictionary containing study parameters
        
    Returns:
        Dictionary of compiled software artifacts
    """
    sw_config = get_software_config(study_params)
    artifacts = {}
    
    # Compile each benchmark
    for benchmark in sw_config['benchmarks']:
        artifacts[benchmark] = {}
        
        # Compile for each core configuration
        for core in sw_config['target_cores']:
            artifacts[benchmark][core] = bazel_build(
                target=f"//design/software/{benchmark}:executable",
                config=f"--config={core}"
            )
    
    return artifacts

def main():
    """Main entry point for software compilation flow when run standalone."""
    
    # Create the flow
    with Flow("Software Compilation") as flow:
        # Load a default configuration for standalone execution
        from flows.utils.config import load_config
        config = load_config()
        
        # Run the compilation
        artifacts = compile_software(config)
    
    # Run the flow
    flow_state = flow.run()
    
    return flow_state.is_successful()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
