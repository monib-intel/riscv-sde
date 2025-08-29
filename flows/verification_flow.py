#!/usr/bin/env python3
"""
Stage 0: Environment and Infrastructure Verification Flow

This script verifies that the development environment and infrastructure
are properly set up before running the main PPA study flows.
"""

import os
import sys
import subprocess
from prefect import task, flow
from pathlib import Path
import logging

# Import utilities
from flows.utils.config import load_config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@task
def verify_environment():
    """
    Run environment verification tests using pytest.
    
    Returns:
        Dictionary with verification results
    """
    logger.info("Starting environment verification...")
    
    project_root = Path(__file__).parent.parent.absolute()
    test_file = project_root / "tests" / "test_dependencies.py"
    
    try:
        # Run the dependency tests
        result = subprocess.run(
            ["python", "-m", "pytest", str(test_file), "-v"],
            cwd=str(project_root),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        logger.info("Environment verification completed successfully")
        logger.info(f"Test output:\n{result.stdout}")
        
        return {
            "status": "success",
            "output": result.stdout,
            "tests_passed": True
        }
    
    except subprocess.CalledProcessError as e:
        logger.error(f"Environment verification failed: {e}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        
        return {
            "status": "failed", 
            "output": e.stdout,
            "error": e.stderr,
            "tests_passed": False
        }

@task
def verify_bazel_environment():
    """
    Verify Bazel environment and test Stage 0 target.
    
    Returns:
        Dictionary with Bazel verification results
    """
    logger.info("Verifying Bazel environment...")
    
    project_root = Path(__file__).parent.parent.absolute()
    
    try:
        # Test Bazel version
        version_result = subprocess.run(
            ["bazel", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        logger.info(f"Bazel version: {version_result.stdout.strip()}")
        
        # Test Stage 0 target
        test_result = subprocess.run(
            ["bazel", "test", "//:verify_environment", "--test_output=summary"],
            cwd=str(project_root), 
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        logger.info("Bazel Stage 0 verification completed successfully")
        logger.info(f"Test output:\n{test_result.stdout}")
        
        return {
            "status": "success",
            "bazel_version": version_result.stdout.strip(),
            "test_output": test_result.stdout,
            "tests_passed": True
        }
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Bazel verification failed: {e}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        
        return {
            "status": "failed",
            "test_output": e.stdout,
            "error": e.stderr, 
            "tests_passed": False
        }

@flow(name="Stage 0: Environment Verification")
def verification_flow():
    """Main verification flow for Stage 0."""
    logger.info("Starting Stage 0: Environment Verification")
    
    # Run environment verification
    env_result = verify_environment()
    bazel_result = verify_bazel_environment()
    
    # Check results
    if env_result["tests_passed"] and bazel_result["tests_passed"]:
        logger.info("✅ Stage 0: Environment verification completed successfully!")
        logger.info("Your development environment is ready for the PPA study.")
        return True
    else:
        logger.error("❌ Stage 0: Environment verification failed!")
        logger.error("Please fix the issues above before proceeding.")
        return False

def main():
    """Main entry point for verification flow when run standalone."""
    try:
        result = verification_flow()
        return result
    except Exception as e:
        logger.error(f"Verification flow failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)