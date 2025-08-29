#!/usr/bin/env python3
"""
Test for ensuring dependencies are set up correctly for the silicon design environment.
"""

import os
import sys
import subprocess
import importlib
import pytest
import tomli
from pathlib import Path

# Define the project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()

def test_python_packages():
    """Test that all required Python packages from pyproject.toml are installed."""
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    assert pyproject_path.exists(), "pyproject.toml file not found"
    
    # Map package names to their import names where they differ
    package_import_map = {
        'prefect': 'prefect',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'matplotlib': 'matplotlib',
        'jupyterlab': 'jupyter_server',  # jupyterlab imports jupyter_server
        'scikit-learn': 'sklearn',
        'tqdm': 'tqdm',
        'pytest': 'pytest',
        'pytest-cov': 'pytest_cov',
        'coverage': 'coverage',
        'pyyaml': 'yaml',
        'griffe': 'griffe',
        'dataclasses-json': 'dataclasses_json',
        'typing-inspect': 'typing_inspect',
        'pluggy': 'pluggy',
        'exceptiongroup': 'exceptiongroup',
        'iniconfig': 'iniconfig'
    }
    
    # Packages to temporarily skip checking
    skip_packages = []  # Empty list now that we fixed dependencies
    
    # Read dependencies from pyproject.toml
    with open(pyproject_path, 'rb') as f:
        pyproject_data = tomli.load(f)
    
    # Get main dependencies
    dependencies = pyproject_data.get('project', {}).get('dependencies', [])
    # Get dev dependencies
    dev_dependencies = pyproject_data.get('project', {}).get('optional-dependencies', {}).get('dev', [])
    
    # Combine all dependencies
    all_dependencies = dependencies + dev_dependencies
    
    # Extract package names from dependency strings (removing version specifiers)
    required_packages = []
    for dep in all_dependencies:
        # Split on any of these characters: >=<=~!
        parts = [p for p in dep.replace('>=', ' ').replace('<=', ' ').replace('==', ' ').replace('~=', ' ').replace('!=', ' ').split(' ') if p]
        if parts:
            required_packages.append(parts[0])
    
    missing_packages = []
    for package in required_packages:
        if package in skip_packages:
            continue
            
        try:
            # Use the import name from the map, or the package name itself if not mapped
            import_name = package_import_map.get(package, package.replace('-', '_'))
            importlib.import_module(import_name)
        except ImportError as e:
            missing_packages.append(f"{package} ({str(e)})")
    
    assert not missing_packages, f"Missing required packages: {', '.join(missing_packages)}"

def test_bazel_available():
    """Test that Bazel is available in the system path."""
    try:
        result = subprocess.run(
            ["bazel", "--version"], 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        assert "bazel" in result.stdout.lower(), "Bazel version check failed"
    except (subprocess.SubprocessError, FileNotFoundError):
        pytest.fail("Bazel is not installed or not in the system path")

def test_riscv_toolchain():
    """Test that the RISC-V toolchain is installed and available."""
    # List of essential RISC-V tools that must be present
    essential_tools = [
        "riscv64-unknown-elf-gcc",
        "riscv64-unknown-elf-g++",
        "riscv64-unknown-elf-as",
        "riscv64-unknown-elf-ld",
        "riscv64-unknown-elf-objdump",
        "riscv64-unknown-elf-objcopy",
        "riscv64-unknown-elf-size",
    ]
    
    # List of optional RISC-V tools that are nice to have but not required
    optional_tools = [
        "riscv64-unknown-elf-gdb"
    ]
    
    missing_essential_tools = []
    missing_optional_tools = []
    
    # Check essential tools
    for tool in essential_tools:
        try:
            # Check if the tool exists and can run
            result = subprocess.run(
                [tool, "--version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                missing_essential_tools.append(f"{tool} (exists but returned error code {result.returncode})")
        except FileNotFoundError:
            missing_essential_tools.append(tool)
    
    # Check optional tools
    for tool in optional_tools:
        try:
            result = subprocess.run(
                [tool, "--version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                missing_optional_tools.append(f"{tool} (exists but returned error code {result.returncode})")
        except FileNotFoundError:
            missing_optional_tools.append(tool)
    
    # Print warning for missing optional tools, but don't fail the test
    if missing_optional_tools:
        print(f"WARNING: Missing optional RISC-V tools: {', '.join(missing_optional_tools)}")
    
    # Assert that all essential tools are present
    assert not missing_essential_tools, f"Missing essential RISC-V tools: {', '.join(missing_essential_tools)}"
    
def test_riscv_gcc_functionality():
    """Test that the RISC-V GCC can actually compile a simple program."""
    # Create a temporary directory for the test
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a simple C program without standard library dependencies
        test_c_file = Path(tmpdir) / "test.c"
        with open(test_c_file, "w") as f:
            f.write("""
int main() {
    int a = 1;
    int b = 2;
    return a + b;
}
""")
        
        # Try to compile it
        try:
            result = subprocess.run(
                ["riscv64-unknown-elf-gcc", "-o", str(Path(tmpdir) / "test"), str(test_c_file), "-nostdlib", "-nostartfiles"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # If compilation fails, try a simpler approach - just check if we can create object files
            if result.returncode != 0:
                print(f"Warning: Failed to compile executable: {result.stderr}")
                print("Trying to compile to object file only...")
                
                obj_result = subprocess.run(
                    ["riscv64-unknown-elf-gcc", "-c", "-o", str(Path(tmpdir) / "test.o"), str(test_c_file)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                assert obj_result.returncode == 0, f"Failed to compile test program to object file: {obj_result.stderr}"
                assert (Path(tmpdir) / "test.o").exists(), "Compiled object file not found"
                
                # Verify it's a RISC-V object file
                objdump_result = subprocess.run(
                    ["riscv64-unknown-elf-objdump", "-f", str(Path(tmpdir) / "test.o")],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                assert "riscv" in objdump_result.stdout.lower(), "Compiled object is not for RISC-V architecture"
                
                print("Successfully compiled to RISC-V object file.")
                return
            
            # If we got here, the full executable compilation worked
            assert (Path(tmpdir) / "test").exists(), "Compiled binary not found"
            
            # Verify it's a RISC-V binary
            objdump_result = subprocess.run(
                ["riscv64-unknown-elf-objdump", "-f", str(Path(tmpdir) / "test")],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            assert "riscv" in objdump_result.stdout.lower(), "Compiled binary is not a RISC-V executable"
            
        except FileNotFoundError:
            pytest.fail("RISC-V GCC not found")

def test_project_structure():
    """Test that critical project directories and files exist."""
    # Key directories that should exist
    critical_directories = [
        "analyze",
        "build", 
        "build/configs",
        "build/flows",
        "build/infrastructure",
        "design",
        "validate",
    ]
    
    # Key files that should exist
    critical_files = [
        "WORKSPACE.bazel",
        "MODULE.bazel",
        "pyproject.toml",
        "build/flows/software_flow.py",
        "build/flows/utils/config.py",
        "build/flows/utils/bazel.py",
    ]
    
    for directory in critical_directories:
        dir_path = PROJECT_ROOT / directory
        assert dir_path.exists(), f"Critical directory not found: {directory}"
        assert dir_path.is_dir(), f"Path exists but is not a directory: {directory}"
    
    for file_path in critical_files:
        full_path = PROJECT_ROOT / file_path
        assert full_path.exists(), f"Critical file not found: {file_path}"
        assert full_path.is_file(), f"Path exists but is not a file: {file_path}"

def test_config_loading():
    """Test that configuration loading works correctly."""
    # Import the configuration utilities
    sys.path.insert(0, str(PROJECT_ROOT))
    from build.flows.utils.config import load_config, get_software_config
    
    # Test default config loading
    config = load_config()
    assert isinstance(config, dict), "Configuration should be a dictionary"
    assert "cores" in config, "Configuration should have 'cores' key"
    assert "benchmarks" in config, "Configuration should have 'benchmarks' key"
    
    # Test software config extraction
    sw_config = get_software_config(config)
    assert "benchmarks" in sw_config, "Software config should have 'benchmarks' key"
    assert "target_cores" in sw_config, "Software config should have 'target_cores' key"

def test_bazel_build_function():
    """Test that the bazel_build function is properly defined."""
    # Import the bazel utility
    sys.path.insert(0, str(PROJECT_ROOT))
    from build.flows.utils.bazel import bazel_build
    
    # Test function existence and signature
    assert callable(bazel_build), "bazel_build should be a callable function"
    
    # We're not actually running bazel here, just verifying the function exists
    # A mock could be used for more thorough testing if needed

if __name__ == "__main__":
    pytest.main(["-v", __file__])
