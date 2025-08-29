#!/usr/bin/env python3
"""
Analysis Flow

This script handles the analysis of simulation and synthesis results,
generating PPA (Power, Performance, Area) reports and visualizations.
"""

import os
import sys
from prefect import task, Flow

# Import utilities
from flows.utils.config import get_analysis_config
from flows.utils.visualization import generate_plots, generate_report

@task
def analyze_results(sim_results, synth_results, study_params):
    """
    Analyze simulation and synthesis results to generate PPA reports.
    
    Args:
        sim_results: Dictionary of simulation results
        synth_results: Dictionary of synthesis results
        study_params: Dictionary containing study parameters
        
    Returns:
        Dictionary of analysis results and paths to reports
    """
    analysis_config = get_analysis_config(study_params)
    results = {
        'power': {},
        'performance': {},
        'area': {},
        'reports': {},
        'visualizations': {}
    }
    
    # Analyze each core
    for core in sim_results:
        results['performance'][core] = {}
        
        # Extract performance metrics from simulation results
        for benchmark in sim_results[core]:
            results['performance'][core][benchmark] = {
                'cycles': sim_results[core][benchmark].get('cycles', 0),
                'instructions': sim_results[core][benchmark].get('instructions', 0),
                'cpi': sim_results[core][benchmark].get('cycles', 0) / 
                      max(1, sim_results[core][benchmark].get('instructions', 1))
            }
    
    # For each synthesized core
    for core in synth_results:
        results['power'][core] = {}
        results['area'][core] = {}
        
        # For each PDK
        for pdk in synth_results[core]:
            results['power'][core][pdk] = {}
            results['area'][core][pdk] = {}
            
            # For each benchmark
            for benchmark in synth_results[core][pdk]:
                # Extract power and area metrics
                pr_results = synth_results[core][pdk][benchmark]['place_and_route']
                
                results['power'][core][pdk][benchmark] = {
                    'dynamic': pr_results.get('dynamic_power', 0),
                    'leakage': pr_results.get('leakage_power', 0),
                    'total': pr_results.get('total_power', 0)
                }
                
                results['area'][core][pdk][benchmark] = {
                    'logic': pr_results.get('logic_area', 0),
                    'memory': pr_results.get('memory_area', 0),
                    'total': pr_results.get('total_area', 0),
                    'utilization': pr_results.get('utilization', 0)
                }
    
    # Generate visualizations
    results['visualizations'] = generate_plots(
        results, 
        output_dir=analysis_config.get('output_dir', 'analysis/targets/plots')
    )
    
    # Generate reports
    results['reports'] = generate_report(
        results,
        study_params,
        output_dir=analysis_config.get('output_dir', 'analysis/targets/reports')
    )
    
    return results

def main():
    """Main entry point for analysis flow when run standalone."""
    
    # Create the flow
    with Flow("PPA Analysis") as flow:
        # Load a default configuration for standalone execution
        from flows.utils.config import load_config
        from flows.software_flow import compile_software
        from flows.simulation_flow import run_simulations
        from flows.synthesis_flow import run_synthesis
        
        config = load_config()
        sw_artifacts = compile_software(config)
        sim_results = run_simulations(sw_artifacts, config)
        synth_results = run_synthesis(sim_results, config)
        
        # Run the analysis
        analysis_results = analyze_results(sim_results, synth_results, config)
    
    # Run the flow
    flow_state = flow.run()
    
    return flow_state.is_successful()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
