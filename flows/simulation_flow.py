#!/usr/bin/env python3
"""
RTL Simulation Flow

This script handles the RTL simulation of RISC-V cores with compiled software,
collecting performance metrics and generating switching activity for power analysis.
"""

import os
import sys
from prefect import task, flow
import logging

# Import utilities
from flows.utils.config import get_simulation_config, load_config
from flows.utils.tools import run_verilator, run_vcs

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@task
def run_simulations(sw_artifacts, study_params):
    """
    Run RTL simulations for each core with the compiled software.
    
    Args:
        sw_artifacts: Dictionary of compiled software artifacts
        study_params: Dictionary containing study parameters
        
    Returns:
        Dictionary of simulation results
    """
    sim_config = get_simulation_config(study_params)
    results = {}
    
    # For each core
    for core in sim_config['cores']:
        results[core] = {}
        
        # For each benchmark
        for benchmark, artifacts in sw_artifacts.items():
            if core in artifacts:
                # Run simulation
                simulator = sim_config['cores'][core].get('simulator', 'verilator')
                if simulator == 'verilator':
                    results[core][benchmark] = run_verilator(
                        core_rtl=f"design/hardware/rtl/cores/{core}",
                        testbench=f"design/hardware/rtl/testbench/universal_tb.sv",
                        executable=artifacts[core],
                        options=sim_config['cores'][core].get('options', {})
                    )
                elif simulator == 'vcs':
                    results[core][benchmark] = run_vcs(
                        core_rtl=f"design/hardware/rtl/cores/{core}",
                        testbench=f"design/hardware/rtl/testbench/universal_tb.sv",
                        executable=artifacts[core],
                        options=sim_config['cores'][core].get('options', {})
                    )
                else:
                    raise ValueError(f"Unsupported simulator: {simulator}")
    
    return results

@flow(name="RTL Simulation Flow")
def simulation_flow():
    """Main RTL simulation flow."""
    logger.info("Starting Stage 2: RTL Simulation")
    
    # Load configuration and compile software first
    config = load_config()
    from flows.software_flow import compile_software
    sw_artifacts = compile_software(config)
    
    # Run the simulations
    sim_results = run_simulations(sw_artifacts, config)
    
    logger.info("✅ Stage 2: RTL simulation completed successfully!")
    return sim_results

def main():
    """Main entry point for simulation flow when run standalone."""
    try:
        result = simulation_flow()
        return True
    except Exception as e:
        logger.error(f"Simulation flow failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
