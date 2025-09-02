#!/usr/bin/env python3
"""
Simple script to test building the hello-world example with Bazel.
"""
import os
import subprocess
import sys

def main():
    print("Building hello-world example with Bazel...")
    
    try:
        result = subprocess.run(
            ["bazel", "build", "//design/software/hello-world:executable"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Build succeeded!")
        print(result.stdout)
        
        # Check if the output file exists
        output_file = os.path.join("output", "bazel-bin", "design", "software", "hello-world", "hello_world.hex")
        if os.path.exists(output_file):
            print(f"Output file exists: {output_file}")
        else:
            print(f"Output file does not exist: {output_file}")
            # Try to find the output file
            print("Searching for output files...")
            for root, dirs, files in os.walk("output"):
                for file in files:
                    if file.endswith(".hex"):
                        print(f"Found hex file: {os.path.join(root, file)}")
        
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print(f"Stderr: {e.stderr}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
