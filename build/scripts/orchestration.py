"""
Prefect-based orchestration for the RISC-V Silicon Design Environment.
This script defines flows for building, simulating, and analyzing RISC-V cores.
"""

import os
import subprocess
import tempfile
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from prefect import flow, task
    from prefect.tasks import task_input_hash
    from prefect.context import get_run_context
    PREFECT_AVAILABLE = True
except ImportError:
    # Define dummy decorators if Prefect is not available
    def flow(func=None, **kwargs):
        def wrapper(f):
            return f
        return wrapper if func is None else wrapper(func)
    
    def task(func=None, **kwargs):
        def wrapper(f):
            return f
        return wrapper if func is None else wrapper(func)
    
    # Define a dummy task_input_hash function
    def task_input_hash(*args, **kwargs):
        return None
    
    PREFECT_AVAILABLE = False
    print("Prefect not available. Flows will run without orchestration.")


@task(cache_key_fn=task_input_hash, cache_expiration=3600)
def run_bazel_command(command: List[str], working_dir: Optional[str] = None) -> str:
    """
    Run a Bazel command and return the output.
    
    Args:
        command: Bazel command to run
        working_dir: Working directory (optional)
        
    Returns:
        Command output
    """
    cmd = ["bazel"] + command
    cwd = working_dir or os.getcwd()
    
    print(f"Running Bazel command: {' '.join(cmd)}")
    print(f"Working directory: {cwd}")
    
    result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
    return result.stdout


@task(cache_key_fn=task_input_hash, cache_expiration=3600)
def clean_output_directory(core: str, output_dir: str = "output") -> None:
    """
    Clean the output directory for a specific core.
    
    Args:
        core: Core name
        output_dir: Output directory
    """
    core_dir = Path(output_dir) / f"{core}_sim"
    if core_dir.exists():
        print(f"Cleaning directory: {core_dir}")
        for f in ['program.hex', 'sim_core', 'sim.vcd']:
            file_path = core_dir / f
            if file_path.exists():
                file_path.unlink()


@flow(name="Software Flow")
def software_flow(config_file: str = "build/configs/simple_core_test.yaml", working_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Run the software flow to compile RISC-V programs.
    
    Args:
        config_file: Configuration file path
        working_dir: Working directory for Bazel commands
    
    Returns:
        Flow results
    """
    print(f"Running software flow with config: {config_file}")
    
    # Use Bazel to build the software
    output = run_bazel_command(["build", "//design/software/hello-world:executable"], working_dir=working_dir)
    
    return {
        "status": "success",
        "output": output,
        "config_file": config_file
    }


@flow(name="Simulation Flow")
def simulation_flow(core: str = "simple_core", config_file: str = "build/configs/simple_core_test.yaml", 
                    output_dir: str = "output", clean: bool = False, working_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Run the simulation flow for a specific core.
    
    Args:
        core: Core to simulate
        config_file: Configuration file path
        output_dir: Output directory
        clean: Whether to clean the output directory
        working_dir: Working directory for Bazel commands
    
    Returns:
        Flow results
    """
    print(f"Running simulation flow for core: {core}")
    
    # Clean if requested
    if clean:
        run_bazel_command(["clean"], working_dir=working_dir)
        clean_output_directory(core, output_dir)
    
    # Ensure output directory exists
    os.makedirs(os.path.join(output_dir, f"{core}_sim"), exist_ok=True)
    
    # Set environment variables for the Bazel target
    os.environ["OUTPUT_DIR"] = os.path.join(output_dir, f"{core}_sim")
    os.environ["CONFIG_FILE"] = config_file
    
    # Run the simulation using Bazel
    target = f"//validate/simulations:{core}_simulation"  # Updated path after moving simulations directory
    output = run_bazel_command(["run", target], working_dir=working_dir)
    
    return {
        "status": "success",
        "output": output,
        "core": core,
        "config_file": config_file,
        "output_dir": output_dir
    }


@flow(name="Analysis Flow")
def analysis_flow(core: str = "simple_core", config_file: str = "build/configs/simple_core_test.yaml", 
                 output_dir: str = "output", working_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Run the analysis flow to analyze simulation results.
    
    Args:
        core: Core to analyze
        config_file: Configuration file path
        output_dir: Output directory
        working_dir: Working directory for Bazel commands
    
    Returns:
        Flow results
    """
    print(f"Running analysis flow for core: {core}")
    
    # For now, analysis flow is not fully implemented
    print("Analysis flow is not yet implemented as an executable")
    
    return {
        "status": "skipped",
        "core": core,
        "config_file": config_file,
        "output_dir": output_dir
    }
    
    return {
        "status": "success",
        "output": output,
        "core": core,
        "config_file": config_file,
        "output_dir": output_dir
    }


@flow(name="Main Flow")
def main_flow(core: str = "simple_core", config_file: str = "build/configs/simple_core_test.yaml", 
             output_dir: str = "output", clean: bool = False, build_docs: bool = False, 
             flows: List[str] = ["software", "simulation", "analysis"],
             working_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Run the main flow orchestrating all sub-flows.
    
    Args:
        core: Core to simulate
        config_file: Configuration file path
        output_dir: Output directory
        clean: Whether to clean the output directory
        build_docs: Whether to build documentation
        flows: List of flows to run
        working_dir: Working directory for Bazel commands
    
    Returns:
        Flow results
    """
    results = {}
    
    if "software" in flows:
        results["software"] = software_flow(config_file, working_dir=working_dir)
    
    if "simulation" in flows:
        results["simulation"] = simulation_flow(core, config_file, output_dir, clean, working_dir=working_dir)
    
    if "analysis" in flows:
        results["analysis"] = analysis_flow(core, config_file, output_dir, working_dir=working_dir)
    
    if build_docs:
        # Build docs with Bazel
        output = run_bazel_command(["build", "//docs:html"], working_dir=working_dir)
        results["docs"] = {
            "status": "success",
            "output": output
        }
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run RISC-V Silicon Design Environment flows')
    parser.add_argument('--core', choices=['simple_core', 'picorv32'], 
                        default='simple_core',
                        help='The core to simulate (default: simple_core)')
    parser.add_argument('--clean', action='store_true',
                        help='Clean build artifacts before running')
    parser.add_argument('--output-dir', default='output',
                        help='Directory to store simulation outputs (default: output)')
    parser.add_argument('--config', default='build/configs/simple_core_test.yaml',
                        help='Configuration file to use (default: build/configs/simple_core_test.yaml)')
    parser.add_argument('--build-docs', action='store_true',
                        help='Build documentation')
    parser.add_argument('--flows', default='software,simulation,analysis',
                        help='Comma-separated list of flows to run (default: software,simulation,analysis)')
    parser.add_argument('--working-dir', default=None,
                        help='Working directory for Bazel commands')
    
    args = parser.parse_args()
    
    # Convert flows string to list
    flows_list = args.flows.split(',')
    
    # Run the main flow
    main_flow(
        core=args.core,
        config_file=args.config,
        output_dir=args.output_dir,
        clean=args.clean,
        build_docs=args.build_docs,
        flows=flows_list,
        working_dir=args.working_dir
    )
