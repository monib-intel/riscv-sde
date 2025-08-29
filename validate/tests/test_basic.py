#!/usr/bin/env python3
"""
Basic test file for RISC-V Rust projects.
"""

import sys
import pytest
from pathlib import Path

# Add the tools directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import the regression runner and TestConfig
from tools.regression import RegressionRunner
from tools.config import TestConfig

def test_hello_world_on_picorv32(regression_runner):
    """Test the hello-world project on picorv32."""
    # Create a test configuration
    test_config = TestConfig(
        project_name="hello-world",
        core_name="picorv32",
        expected_output=["Loading program from", "Simulation completed!"],  # Check for these strings in output
        timeout=10000
    )
    
    # Run the test
    success, output, error = regression_runner.run_test(test_config)
    
    # Print the output for debugging
    print("\nSimulation Output:")
    print("-" * 80)
    print(output)
    print("-" * 80)
    
    # Print the expected output
    print("\nExpected Output:")
    print("-" * 80)
    for expected in test_config.expected_output:
        print(f"- {expected}")
    print("-" * 80)
    
    # Print whether each expected output was found
    print("\nOutput Check:")
    print("-" * 80)
    for expected in test_config.expected_output:
        found = expected in output
        print(f"- '{expected}': {'✓ Found' if found else '✗ Not found'}")
    print("-" * 80)
    
    # Assert the test passed
    assert success, f"Test failed: {error}"

def test_hello_world_on_simple_core(regression_runner):
    """Test the hello-world project on simple_core."""
    # Create a test configuration
    test_config = TestConfig(
        project_name="hello-world",
        core_name="simple_core",
        expected_output=["PC: 00000000, INSTR: 00001000", "PC: 00000004, INSTR: 00100093"],
        timeout=10000
    )
    
    # Run the test
    success, output, error = regression_runner.run_test(test_config)
    
    # Print the output for debugging
    print("\nSimulation Output:")
    print("-" * 80)
    print(output)
    print("-" * 80)
    
    # Print the expected output
    print("\nExpected Output:")
    print("-" * 80)
    for expected in test_config.expected_output:
        print(f"- {expected}")
    print("-" * 80)
    
    # Print whether each expected output was found
    print("\nOutput Check:")
    print("-" * 80)
    for expected in test_config.expected_output:
        found = expected in output
        print(f"- '{expected}': {'✓ Found' if found else '✗ Not found'}")
    print("-" * 80)
    
    # Assert the test passed
    assert success, f"Test failed: {error}"

def test_project_discovery(regression_runner):
    """Test that projects are correctly discovered."""
    # Get the list of projects
    projects = regression_runner.list_projects()
    
    # Verify hello-world is in the list
    assert "hello-world" in projects, "hello-world project not found"
    
    # Print discovered projects
    print("\nDiscovered projects:")
    for project in projects:
        print(f"  - {project}")

def test_core_discovery(regression_runner):
    """Test that cores are correctly discovered."""
    # Get the list of cores
    cores = regression_runner.list_cores()
    
    # Verify picorv32 is in the list
    assert "picorv32" in cores, "picorv32 core not found"
    
    # Verify simple_core is in the list
    assert "simple_core" in cores, "simple_core not found"
    
    # Print discovered cores
    print("\nDiscovered cores:")
    for core in cores:
        print(f"  - {core}")

if __name__ == "__main__":
    # When run directly, run the tests
    pytest.main(["-xvs", __file__])
