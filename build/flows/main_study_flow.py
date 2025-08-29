#!/usr/bin/env python3
"""
Main PPA Study Orchestration Flow

This script orchestrates the complete PPA (Power, Performance, Area) study workflow,
coordinating all subflows and tasks to produce comprehensive analysis results.
"""

import os
import sys
from prefect import flow
import logging

# Import subflows
from flows.verification_flow import verification_flow
from flows.software_flow import software_compilation_flow, compile_software
from flows.simulation_flow import simulation_flow, run_simulations
from flows.synthesis_flow import synthesis_flow, run_synthesis
from flows.analysis_flow import analysis_flow, analyze_results

# Import utilities
from flows.utils.config import load_config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@flow(name="RISC-V PPA Study")
def main_ppa_study_flow():
    """Complete RISC-V PPA study orchestration flow."""
    logger.info("🚀 Starting Complete PPA Study Orchestration")
    
    # Load configuration
    config = load_config()
    
    # Stage 0: Verify environment and infrastructure
    logger.info("Stage 0: Verifying environment and infrastructure...")
    env_result = verification_flow()
    
    if not env_result:
        logger.error("❌ Stage 0 failed. Cannot proceed with PPA study.")
        return False
    
    # Stage 1: Compile software for all test cases
    logger.info("Stage 1: Compiling software...")
    sw_artifacts = compile_software(config)
    
    # Stage 2: Run simulations on all cores
    logger.info("Stage 2: Running RTL simulations...")
    sim_results = run_simulations(sw_artifacts, config)
    
    # Stage 3: Run synthesis for all cores and PDKs
    logger.info("Stage 3: Running synthesis and PNR...")
    synth_results = run_synthesis(sim_results, config)
    
    # Stage 4: Analyze the results
    logger.info("Stage 4: Analyzing results and generating reports...")
    final_report = analyze_results(sim_results, synth_results, config)
    
    logger.info("🎉 Complete PPA Study finished successfully!")
    return final_report

def main():
    """Main entry point for the PPA study orchestration."""
    try:
        result = main_ppa_study_flow()
        return result is not False
    except Exception as e:
        logger.error(f"PPA study flow failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
