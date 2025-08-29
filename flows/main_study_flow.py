#!/usr/bin/env python3
"""
Main PPA Study Orchestration Flow

This script orchestrates the complete PPA (Power, Performance, Area) study workflow,
coordinating all subflows and tasks to produce comprehensive analysis results.
"""

import os
import sys
from prefect import Flow, task, case
from prefect.engine.results import LocalResult

# Import subflows
from flows.software_flow import compile_software
from flows.simulation_flow import run_simulations
from flows.synthesis_flow import run_synthesis
from flows.analysis_flow import analyze_results

# Import utilities
from flows.utils.config import load_config
from flows.utils.logging import setup_logging

def main():
    """Main entry point for the PPA study orchestration."""
    
    # Setup logging
    logger = setup_logging("main_study_flow")
    logger.info("Starting PPA study orchestration")
    
    # Load configuration
    config = load_config()
    
    # Create the main flow
    with Flow("RISC-V PPA Study") as flow:
        # Configure study parameters
        study_params = task(lambda: config)()
        
        # Compile software for all test cases
        sw_artifacts = compile_software(study_params)
        
        # Run simulations on all cores
        sim_results = run_simulations(sw_artifacts, study_params)
        
        # Run synthesis for all cores and PDKs
        synth_results = run_synthesis(sim_results, study_params)
        
        # Analyze the results
        final_report = analyze_results(sim_results, synth_results, study_params)
    
    # Run the flow
    flow_state = flow.run()
    
    return flow_state.is_successful()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
