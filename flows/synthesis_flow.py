#!/usr/bin/env python3
"""
Synthesis Flow

This script handles the physical implementation of RISC-V cores,
including synthesis, place and route, and power analysis.
"""

import os
import sys
from prefect import task, Flow

# Import utilities
from flows.utils.config import get_synthesis_config
from flows.utils.tools import run_yosys, run_openroad

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

def main():
    """Main entry point for synthesis flow when run standalone."""
    
    # Create the flow
    with Flow("Synthesis and P&R") as flow:
        # Load a default configuration for standalone execution
        from flows.utils.config import load_config
        from flows.software_flow import compile_software
        from flows.simulation_flow import run_simulations
        
        config = load_config()
        sw_artifacts = compile_software(config)
        sim_results = run_simulations(sw_artifacts, config)
        
        # Run the synthesis
        synth_results = run_synthesis(sim_results, config)
    
    # Run the flow
    flow_state = flow.run()
    
    return flow_state.is_successful()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
