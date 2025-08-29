"""
Bazel utilities for building software and RTL.
"""

import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def bazel_build(target, config=None, options=None):
    """
    Build a target using Bazel.
    
    Args:
        target: Target to build (e.g. //design/software/fft:executable)
        config: Optional configuration to use (e.g. --config=rocket)
        options: Additional options to pass to Bazel
        
    Returns:
        Dictionary with paths to built artifacts
    """
    cmd = ["bazel", "build"]
    
    # Add configuration if specified
    if config:
        cmd.append(config)
    
    # Add additional options
    if options:
        if isinstance(options, list):
            cmd.extend(options)
        elif isinstance(options, str):
            cmd.append(options)
        else:
            for key, value in options.items():
                cmd.append(f"--{key}={value}")
    
    # Add target
    cmd.append(target)
    
    logger.info(f"Running Bazel command: {' '.join(cmd)}")
    
    # Run the command
    try:
        result = subprocess.run(
            cmd, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Parse output to find built artifacts
        output_path = None
        for line in result.stdout.splitlines():
            if line.startswith("bazel-bin"):
                output_path = line.strip()
        
        if not output_path and target.endswith(":executable"):
            # Try to infer the output path
            parts = target.split(":")
            if len(parts) == 2:
                target_path = parts[0].lstrip("/")
                output_path = os.path.join("bazel-bin", target_path, "executable")
        
        return {
            "path": output_path,
            "target": target,
            "success": True
        }
    
    except subprocess.CalledProcessError as e:
        logger.error(f"Bazel build failed: {e}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        
        return {
            "path": None,
            "target": target,
            "success": False,
            "error": e.stderr
        }
