# Project Structure

The RISC-V Silicon Design Environment is organized in a modular structure to separate different components of the design flow. This document provides an overview of the project's directory structure and the purpose of each component.

## Top-Level Directories

```
silicon-design-environment/
├── build/              # Build infrastructure and flows
├── design/             # RTL and software designs
├── docs/               # Documentation
├── output/             # Generated outputs
└── validate/           # Validation, testing, and simulations
```

## Build Infrastructure (`build/`)

The `build/` directory contains all the infrastructure for building, simulating, and analyzing designs:

```
build/
├── configs/            # Configuration files
├── flows/              # Flow definitions
│   ├── analysis_flow.py
│   ├── main_study_flow.py
│   ├── simulation_flow.py
│   ├── software_flow.py
│   └── synthesis_flow.py
├── infrastructure/     # Cloud and infrastructure setup
└── scripts/            # Build scripts
    └── orchestration.py # Prefect-based orchestration
```

### Configuration Files (`build/configs/`)

Configuration files define parameters for different flows and cores. They are typically in YAML format and specify cores, benchmarks, and simulation parameters.

Example configuration file:
```yaml
cores: 
  - simple_core
benchmarks:
  - hello-world
cores_config:
  simple_core:
    simulator: verilator
    options:
      trace: true
      max_cycles: 10000
output_dir: output/simple_core_test
```

### Flows (`build/flows/`)

Flow modules define different stages of the silicon design process:

- **software_flow.py**: Compiles software for RISC-V targets
- **simulation_flow.py**: Configures and runs RTL simulations
- **synthesis_flow.py**: Handles logic synthesis flow
- **analysis_flow.py**: Analyzes simulation and synthesis results
- **main_study_flow.py**: Orchestrates all flows together

### Infrastructure (`build/infrastructure/`)

Contains configuration files and scripts for running flows in cloud or Kubernetes environments.

## Design (`design/`)

The `design/` directory contains both hardware and software components:

```
design/
├── hardware/           # Hardware designs
│   ├── physical/       # Physical design files
│   │   ├── common/     # Common PDK files
│   │   └── pdks/       # Process Design Kits
│   └── rtl/            # RTL design files
│       ├── common/     # Common RTL modules
│       ├── cores/      # RISC-V core implementations
│       ├── simulation/ # Simulation-specific modules
│       └── testbench/  # Testbenches
└── software/           # Software applications
    ├── common/         # Common utilities
    ├── crypto/         # Cryptography benchmarks
    ├── fft/            # FFT implementations
    ├── hello-world/    # Simple "Hello World" program
    └── matrix_mult/    # Matrix multiplication
```

### Hardware (`design/hardware/`)

Hardware designs are separated into:

- **RTL designs**: Verilog/SystemVerilog implementations of RISC-V cores and supporting modules
- **Physical designs**: Files related to physical implementation like floorplans, constraints, etc.
- **PDKs**: Process Design Kit files for different technology nodes

### Software (`design/software/`)

Software includes various benchmark programs that can be compiled and run on the RISC-V cores:

- **hello-world**: A simple "Hello World" program, useful for basic testing
- **crypto**: Cryptographic algorithm implementations
- **fft**: Fast Fourier Transform implementations
- **matrix_mult**: Matrix multiplication benchmarks

## Output (`output/`)

The `output/` directory contains all generated files from flows:

```
output/
├── hello_world.hex     # Compiled software binary
├── program.hex         # Program memory image
├── sim_core            # Simulation binary
└── simple_core_sim/    # Simulation outputs
    ├── program.hex     # Copy of program memory image
    ├── sim_core        # Copy of simulation binary
    └── sim.vcd         # Simulation waveform dump
```

## Root Files

Several important files exist at the root of the project:

- **BUILD.bazel**: Main Bazel build file
- **MODULE.bazel**: Bazel module definition
- **WORKSPACE.bazel**: Bazel workspace definition
- **pyproject.toml**: Python project configuration
- **README.md**: Project overview
- **run_with_bazel.sh**: Convenience script for running simulations and flows with Bazel
