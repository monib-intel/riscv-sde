#!/usr/bin/env python3
"""
Synthesis Flow

This script handles the physical implementation of RISC-V cores,
including synthesis, place and route, and power analysis.
"""

import os
import sys
from prefect import task, flow
import logging

# Import utilities
from flows.utils.config import get_synthesis_config, load_config
from flows.utils.tools import run_yosys, run_openroad

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@task
def run_synthesis(sim_results, study_params):
    """
    Run synthesis and physical implementation for each core with the specified PDKs.
    
    Args:
        sim_results: Dictionary of simulation results (including switching activity)
        study_params: Dictionary containing study parameters
        
    Returns:
        Dictionary of synthesis results
    """
    synth_config = get_synthesis_config(study_params)
    results = {}
    
    # For each core
    for core in synth_config['cores']:
        results[core] = {}
        
        # For each PDK
        for pdk in synth_config['pdks']:
            results[core][pdk] = {}
            
            # For each benchmark (to use switching activity)
            for benchmark in sim_results.get(core, {}):
                # Run synthesis
                syn_tool = synth_config['cores'][core].get('syn_tool', 'yosys')
                if syn_tool == 'yosys':
                    synth_result = run_yosys(
                        core_rtl=f"design/hardware/rtl/cores/{core}",
                        pdk=f"design/hardware/physical/{pdk}",
                        options=synth_config['cores'][core].get('syn_options', {})
                    )
                else:
                    raise ValueError(f"Unsupported synthesis tool: {syn_tool}")
                
                # Run place and route
                pr_tool = synth_config['cores'][core].get('pr_tool', 'openroad')
                if pr_tool == 'openroad':
                    pr_result = run_openroad(
                        netlist=synth_result['netlist'],
                        pdk=f"design/hardware/physical/{pdk}",
                        switching=sim_results[core][benchmark].get('switching', None),
                        options=synth_config['cores'][core].get('pr_options', {})
                    )
                else:
                    raise ValueError(f"Unsupported P&R tool: {pr_tool}")
                
                # Store results
                results[core][pdk][benchmark] = {
                    'synthesis': synth_result,
                    'place_and_route': pr_result
                }
    
    return results

@flow(name="Synthesis and PNR Flow")
def synthesis_flow():
    """Main synthesis and P&R flow."""
    logger.info("Starting Stage 3: Synthesis and PNR")
    
    # Load configuration and run prerequisite flows
    config = load_config()
    from flows.software_flow import compile_software
    from flows.simulation_flow import run_simulations
    
    sw_artifacts = compile_software(config)
    sim_results = run_simulations(sw_artifacts, config)
    
    # Run the synthesis
    synth_results = run_synthesis(sim_results, config)
    
    logger.info("✅ Stage 3: Synthesis and PNR completed successfully!")
    return synth_results

def main():
    """Main entry point for synthesis flow when run standalone."""
    try:
        result = synthesis_flow()
        return True
    except Exception as e:
        logger.error(f"Synthesis flow failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
