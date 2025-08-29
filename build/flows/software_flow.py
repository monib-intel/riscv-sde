#!/usr/bin/env python3
"""
Software Compilation Flow

This script handles the compilation of software benchmarks for various RISC-V cores,
producing binaries and executable files for simulation and analysis.
"""

import os
import sys
from prefect import task, flow
import logging

# Import utilities
from flows.utils.config import get_software_config, load_config
from flows.utils.bazel import bazel_build

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@flow(name="Software Compilation Flow")
def software_compilation_flow():
    """Main software compilation flow."""
    logger.info("Starting Stage 1: Software Compilation")
    
    # Load configuration
    config = load_config()
    
    # Run the compilation
    artifacts = compile_software(config)
    
    logger.info("✅ Stage 1: Software compilation completed successfully!")
    return artifacts

def main():
    """Main entry point for software compilation flow when run standalone."""
    try:
        result = software_compilation_flow()
        return True
    except Exception as e:
        logger.error(f"Software compilation flow failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
