#!/usr/bin/env python3
"""
Script to build Sphinx documentation.
This is used by the Bazel sphinx_doc rule.
"""

import argparse
import os
import subprocess
import sys
import tempfile
import shutil

def main():
    """Main function to build Sphinx documentation."""
    parser = argparse.ArgumentParser(description='Build Sphinx documentation')
    parser.add_argument('--src-dir', required=True,
                        help='Source directory containing Sphinx docs')
    parser.add_argument('--build-dir', required=True,
                        help='Output directory for built docs')
    parser.add_argument('--format', default='html',
                        help='Output format (html, pdf, etc.)')
    
    args = parser.parse_args()
    
    # Create a temporary directory for requirements
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract requirements file path from src-dir
        # The src-dir is the location of the conf.py file, which is in docs/
        docs_dir = os.path.dirname(args.src_dir)
        requirements_file = os.path.join(docs_dir, 'requirements.txt')
        
        # Install dependencies
        if os.path.exists(requirements_file):
            print(f"Installing documentation dependencies from {requirements_file}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', requirements_file],
                          check=True)
        
        # Build the documentation
        print(f"Building {args.format} documentation...")
        output_dir = os.path.join(args.build_dir, args.format)
        os.makedirs(output_dir, exist_ok=True)
        
        # Run sphinx-build
        cmd = [
            'sphinx-build',
            '-b', args.format,
            docs_dir,
            output_dir
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=False)
        
        if result.returncode != 0:
            print("Error: Documentation build failed")
            sys.exit(1)
        
        print(f"Documentation built successfully in {output_dir}")

if __name__ == "__main__":
    main()
