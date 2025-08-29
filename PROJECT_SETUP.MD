# RISC-V Silicon Design Environment - Project Setup Guide

This guide will help you set up and use the RISC-V PPA (Power, Performance, Area) Study environment.

## Prerequisites

Before you begin, ensure that you have the following tools installed:

- **Bazel** (version 6.0 or later): Build system for software and hardware
- **Python** (version 3.11 or later): For running the flow orchestration scripts
- **RISC-V Toolchain**: For compiling software to RISC-V ISA
- **Verilator**: For RTL simulation
- **Yosys/OpenROAD**: For synthesis and physical implementation
- **Git**: For version control
- **Kubernetes** (optional): For distributed execution

## Quick Start

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/monib-intel/silicon-design-environment.git
cd silicon-design-environment

# Initialize submodules (if any)
git submodule update --init --recursive
```

### 2. Set Up Development Environment

You can set up the development environment in one of two ways:

#### Option A: Using Nix

Nix provides a reproducible development environment with all tools pre-configured:

```bash
# Install Nix if you don't have it
curl -L https://nixos.org/nix/install | sh

# Enter the Nix shell
cd infrastructure/nix
nix-shell
```

#### Option B: Manual Installation with uv (Recommended)

We use uv for fast, reliable Python dependency management:

```bash
# Install uv if you don't have it
curl -sSf https://astral.sh/uv/install.sh | bash

# Set up everything with one command
./setup.sh
```

The setup script will:
1. Create a virtual environment if it doesn't exist
2. Activate the virtual environment
3. Install all dependencies from pyproject.toml
4. Run tests to verify the installation

Alternatively, you can install dependencies manually:

```bash
# Create and activate a virtual environment
uv venv
source .venv/bin/activate

# Install all dependencies including development dependencies
uv pip install -e ".[dev]"
```

### 3. Install RISC-V Toolchain

The RISC-V GNU Toolchain is required for compiling software for RISC-V processors. You can install it using the following instructions:

```bash
# Clone the repository
git clone https://github.com/riscv/riscv-gnu-toolchain
cd riscv-gnu-toolchain

# Install prerequisites (Ubuntu/Debian)
sudo apt-get install autoconf automake autotools-dev curl python3 python3-pip libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev ninja-build

# Configure and build (newlib)
./configure --prefix=/opt/riscv
sudo make -j$(nproc)

# Optional: Install GDB (if you need debugging capabilities)
# sudo make -j$(nproc) build-gdb

# Add to PATH
echo 'export PATH=$PATH:/opt/riscv/bin' >> ~/.bashrc
source ~/.bashrc
```

To verify the installation, run:

```bash
riscv64-unknown-elf-gcc --version
```

### 4. Verify Installation

Run the dependency tests to ensure everything is set up correctly:

```bash
python -m pytest tests/test_dependencies.py -v
```

This will check for:
- Required Python packages
- Bazel installation
- RISC-V toolchain availability
- Project structure

## Project Structure

The project is organized into the following main directories:

- `design/`: Hardware and software designs under study
  - `hardware/`: RTL cores and physical implementation
  - `software/`: Benchmark applications
- `flows/`: Process definitions and orchestration
- `infrastructure/`: Development and execution environment
- `analysis/`: Results processing and visualization
- `docs/`: Documentation
- `configs/`: Configuration files
- `dependencies/`: Git submodules and external dependencies
- `third_party/`: Third-party libraries and tools

## Running a PPA Study

### 1. Configure Your Study

Edit the configuration file to specify cores, benchmarks, and PDKs:

```bash
vim configs/default.yaml
```

### 2. Run the Complete Flow

```bash
# Run the complete PPA study
python flows/main_study_flow.py --config configs/default.yaml
```

### 3. Run Individual Flows

You can also run individual parts of the flow:

```bash
# Compile software only
python flows/software_flow.py --config configs/default.yaml

# Run RTL simulations
python flows/simulation_flow.py --config configs/default.yaml

# Run synthesis and physical implementation
python flows/synthesis_flow.py --config configs/default.yaml

# Generate analysis and visualizations
python flows/analysis_flow.py --config configs/default.yaml
```

## Using Kubernetes for Distributed Execution

For large studies, you can distribute the workload using Kubernetes:

```bash
# Apply Kubernetes configuration
kubectl apply -f infrastructure/kubernetes/config.yaml
kubectl apply -f infrastructure/kubernetes/job.yaml

# Check job status
kubectl get jobs -n silicon-design
kubectl logs job/riscv-ppa-study -n silicon-design
```

## Adding New Components

### Adding a New Core

1. Create RTL in `design/hardware/rtl/cores/<core_name>/`
2. Add core configuration to your config file
3. Update testbench if needed

### Adding a New Benchmark

1. Create benchmark code in `design/software/<benchmark_name>/`
2. Add build rules in Bazel
3. Add benchmark configuration to your config file

### Adding a New PDK

1. Add PDK files to `design/hardware/physical/<pdk_name>/`
2. Update synthesis scripts to support the new PDK
3. Add PDK configuration to your config file

### Adding External Dependencies

If you need to add external git repositories as dependencies:

```bash
# Add the repository as a submodule
git submodule add https://github.com/username/repo.git dependencies/repo-name

# Initialize and update the submodule
git submodule update --init --recursive

# Reference the dependency in Bazel
# Edit WORKSPACE.bazel or MODULE.bazel as needed
```

## Troubleshooting

### Common Issues

- **Bazel build fails**: Ensure Bazel is properly installed and WORKSPACE file is correctly configured
- **Simulation errors**: Check RTL and testbench for compatibility issues
- **Synthesis errors**: Verify PDK configuration and ensure RTL is synthesizable
- **Flow orchestration errors**: Check Python dependencies and configuration files
- **Python dependency issues**: Run `uv pip install --upgrade -r requirements.txt` to ensure all dependencies are up to date

### Getting Help

If you encounter issues:

1. Check the logs in `logs/` directory
2. Consult the documentation in `docs/` directory
3. Open an issue on GitHub

## Contributing

We welcome contributions to the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please follow the coding style guidelines and add tests for new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
