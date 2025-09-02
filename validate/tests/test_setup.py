#!/usr/bin/env python3
"""
Simple script to test the repository setup.
"""
import os
import subprocess
import sys
import yaml

def run_command(cmd, description=""):
    """Run a command and handle errors."""
    if description:
        print(f"🔧 {description}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                               capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        return True, result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False, e

def test_bazel_build():
    """Test that Bazel can build the hello-world example."""
    print("Testing Bazel build for hello-world...")
    
    success, _ = run_command(
        "bazel build //design/software/hello-world:executable",
        "Building hello-world with Bazel"
    )
    
    if success:
        print("✅ Bazel build succeeded!")
    else:
        print("❌ Bazel build failed!")
    
    return success

def test_python_environment():
    """Test that the Python environment is set up correctly."""
    print("Testing Python environment...")
    
    try:
        import numpy
        import pandas
        import matplotlib
        import prefect
        print("✅ Python environment is set up correctly!")
        return True
    except ImportError as e:
        print(f"❌ Python environment is not set up correctly: {e}")
        return False

def test_riscv_toolchain():
    """Test that the RISC-V toolchain is installed."""
    print("Testing RISC-V toolchain...")
    
    success, _ = run_command(
        "riscv64-unknown-elf-gcc --version",
        "Checking RISC-V GCC version"
    )
    
    if success:
        print("✅ RISC-V toolchain is installed!")
    else:
        print("❌ RISC-V toolchain is not installed!")
    
    return success

def main():
    """Main function to run all tests."""
    print("=== Testing RISC-V SDE Setup ===")
    
    # Test Python environment
    python_ok = test_python_environment()
    
    # Test RISC-V toolchain
    riscv_ok = test_riscv_toolchain()
    
    # Test Bazel build
    bazel_ok = test_bazel_build()
    
    # Summary
    print("\n=== Setup Test Results ===")
    print(f"Python Environment: {'✅' if python_ok else '❌'}")
    print(f"RISC-V Toolchain: {'✅' if riscv_ok else '❌'}")
    print(f"Bazel Build: {'✅' if bazel_ok else '❌'}")
    
    if python_ok and riscv_ok and bazel_ok:
        print("\n✅ All tests passed! Your environment is set up correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues before continuing.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
