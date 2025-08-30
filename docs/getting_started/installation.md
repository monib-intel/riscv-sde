# Installation Guide

This guide will help you install all the necessary components for the RISC-V Silicon Design Environment.

## System Requirements

- **Operating System**: Linux (Ubuntu 20.04+ or equivalent)
- **Memory**: 16GB RAM recommended (8GB minimum)
- **Storage**: 20GB free disk space
- **CPU**: Multi-core processor recommended

## Prerequisites

Before you begin, ensure that you have the following tools installed:

- **Bazel** (version 6.0 or later): Build system for software and hardware
- **Python** (version 3.11 or later): For running the flow orchestration scripts
- **RISC-V Toolchain**: For compiling software to RISC-V ISA
- **Verilator**: For RTL simulation
- **Yosys/OpenROAD**: For synthesis and physical implementation
- **Git**: For version control
- **Kubernetes** (optional): For distributed execution

## Installation Steps

### 1. Install System Dependencies

```bash
# For Ubuntu/Debian
sudo apt update
sudo apt install -y build-essential git python3-dev python3-pip \
    cmake ninja-build pkg-config libffi-dev libssl-dev

# For Python dependencies
pip install -e .

# For Prefect orchestration (optional)
pip install -e ".[orchestration]"
```

### 2. Install Bazel

```bash
# Install Bazelisk (recommended way to install Bazel)
npm install -g @bazel/bazelisk

# Or for direct Bazel installation
wget https://github.com/bazelbuild/bazel/releases/download/6.0.0/bazel-6.0.0-installer-linux-x86_64.sh
chmod +x bazel-6.0.0-installer-linux-x86_64.sh
./bazel-6.0.0-installer-linux-x86_64.sh --user
```

### 3. Install RISC-V Toolchain

```bash
# Download and build the RISC-V GNU toolchain
git clone https://github.com/riscv/riscv-gnu-toolchain
cd riscv-gnu-toolchain
./configure --prefix=/opt/riscv --with-arch=rv32i --with-abi=ilp32
make -j$(nproc)

# Add to PATH
echo 'export PATH=$PATH:/opt/riscv/bin' >> ~/.bashrc
source ~/.bashrc
```

### 4. Install Verilator

```bash
# Install dependencies
sudo apt-get install -y perl make autoconf g++ flex bison ccache
sudo apt-get install -y libgoogle-perftools-dev numactl perl-doc
sudo apt-get install -y libfl2 libfl-dev zlib1g zlib1g-dev

# Download and build Verilator
git clone https://github.com/verilator/verilator
cd verilator
git checkout v4.228  # or the latest stable version
autoconf
./configure
make -j$(nproc)
sudo make install
```

### 5. Install Yosys and OpenROAD

```bash
# Install Yosys
sudo apt-get install -y yosys

# Install OpenROAD
git clone --recursive https://github.com/The-OpenROAD-Project/OpenROAD.git
cd OpenROAD
mkdir build
cd build
cmake ..
make -j$(nproc)
sudo make install
```

### 6. Optional: Kubernetes Setup

If you plan to use the distributed execution features:

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Install minikube for local testing
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube-linux-amd64
sudo mv minikube-linux-amd64 /usr/local/bin/minikube
```

## Verification

To verify that everything is installed correctly:

```bash
# Verify RISC-V toolchain
riscv32-unknown-elf-gcc --version

# Verify Verilator
verilator --version

# Verify Yosys
yosys -V

# Verify Bazel
bazel --version

# Run the project's validation tests
cd silicon-design-environment
pytest validate/tests/
```

## Next Steps

Once you have completed the installation, proceed to the [Quick Start Guide](quickstart.md) to build your first project.
