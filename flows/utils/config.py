"""
Configuration utilities for the PPA study flows.
"""

import os
import yaml
import json

def load_config(config_path=None):
    """
    Load configuration from YAML or JSON file.
    
    Args:
        config_path: Path to configuration file (default: configs/default.yaml)
        
    Returns:
        Dictionary with configuration
    """
    if config_path is None:
        # Try to find a default config
        if os.path.exists('configs/default.yaml'):
            config_path = 'configs/default.yaml'
        elif os.path.exists('configs/default.json'):
            config_path = 'configs/default.json'
        else:
            # Return a minimal default configuration
            return {
                'cores': ['rocket', 'vexriscv', 'cva6'],
                'pdks': ['sky130', 'generic'],
                'benchmarks': ['fft', 'matrix_mult', 'crypto'],
                'output_dir': 'analysis/targets'
            }
    
    # Load from file
    if config_path.endswith('.yaml') or config_path.endswith('.yml'):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    elif config_path.endswith('.json'):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        raise ValueError(f"Unsupported config file format: {config_path}")

def get_software_config(study_params):
    """Extract software-specific configuration."""
    return {
        'benchmarks': study_params.get('benchmarks', []),
        'target_cores': study_params.get('cores', []),
        'compiler': study_params.get('compiler', 'gcc'),
        'compiler_flags': study_params.get('compiler_flags', '-O2')
    }

def get_simulation_config(study_params):
    """Extract simulation-specific configuration."""
    return {
        'cores': study_params.get('cores_config', {}),
        'max_cycles': study_params.get('max_simulation_cycles', 10000000),
        'trace_enabled': study_params.get('enable_trace', False)
    }

def get_synthesis_config(study_params):
    """Extract synthesis-specific configuration."""
    return {
        'cores': study_params.get('cores_config', {}),
        'pdks': study_params.get('pdks', []),
        'clock_period': study_params.get('clock_period_ns', 10.0),
        'utilization_target': study_params.get('utilization_target', 0.7)
    }

def get_analysis_config(study_params):
    """Extract analysis-specific configuration."""
    return {
        'output_dir': study_params.get('output_dir', 'analysis/targets'),
        'plot_format': study_params.get('plot_format', 'png'),
        'report_format': study_params.get('report_format', 'html'),
        'comparison_baseline': study_params.get('comparison_baseline', 'rocket')
    }
