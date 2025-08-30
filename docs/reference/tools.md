# Tools Reference

The RISC-V Silicon Design Environment integrates various tools for design, simulation, synthesis, and analysis. This document provides an overview of these tools and how they are used in the environment.

## RISC-V Toolchain

The RISC-V toolchain is used to compile software for RISC-V targets.

### Components

- **GCC/LLVM Compiler**: Compiles C/C++ code to RISC-V assembly
- **Assembler**: Assembles RISC-V assembly into object code
- **Linker**: Links object files into executables
- **Binary Utilities**: Creates binary and hex files for simulation

### Usage in Flows

The toolchain is primarily used in the software flow:

```bash
python build/flows/software_flow.py --config build/configs/simple_core_test.yaml
```

### Configuration

Toolchain options can be configured in the YAML configuration files:

```yaml
software_config:
  toolchain: riscv32-unknown-elf
  optimization: -O2
  debug: true
  arch: rv32i
  abi: ilp32
```

## Verilator

Verilator is an open-source RTL simulator used for simulating RISC-V cores.

### Features

- Fast cycle-accurate simulation
- VCD waveform generation
- SystemVerilog support
- C++ testbench integration

### Usage in Flows

Verilator is primarily used in the simulation flow:

```bash
python build/flows/simulation_flow.py --config build/configs/simple_core_test.yaml
```

### Configuration

Verilator options can be configured in the YAML configuration files:

```yaml
cores_config:
  simple_core:
    simulator: verilator
    options:
      trace: true
      max_cycles: 10000
      timeout: 300
      verilator_flags: "--trace-fst --trace-structs"
```

## Yosys

Yosys is an open-source synthesis tool used for logic synthesis.

### Features

- RTL synthesis
- Technology mapping
- Formal verification
- Various optimization passes

### Usage in Flows

Yosys is primarily used in the synthesis flow:

```bash
python build/flows/synthesis_flow.py --config build/configs/simple_core_test.yaml
```

### Configuration

Yosys options can be configured in the YAML configuration files:

```yaml
synthesis_config:
  tool: yosys
  technology: sky130
  clock_period: 10  # in ns
  optimization: area  # area or speed
```

## OpenROAD

OpenROAD is an integrated tool for physical design.

### Features

- Floorplanning
- Placement
- Routing
- Timing analysis
- Power analysis

### Usage in Flows

OpenROAD is used in the synthesis and physical design flows:

```bash
python build/flows/synthesis_flow.py --config build/configs/simple_core_test.yaml --physical
```

### Configuration

OpenROAD options can be configured in the YAML configuration files:

```yaml
physical_config:
  tool: openroad
  target_utilization: 0.7
  aspect_ratio: 1.0
  core_margins: 10.0
```

## Bazel

Bazel is the build system used for the entire environment.

### Features

- Hermetic builds
- Incremental compilation
- Parallel execution
- Cross-compilation support

### Usage

Bazel is used to build all software and hardware components:

```bash
# Build a specific target
bazel build //design/software/hello-world:executable

# Build and run a test
bazel test //validate/tests:all

# Build everything
bazel build //...
```

### Configuration

Bazel is configured using:
- `WORKSPACE.bazel`: Defines external dependencies
- `MODULE.bazel`: Defines module configuration
- `BUILD.bazel`: Defines build targets

## GTKWave

GTKWave is used for viewing simulation waveforms.

### Usage

After running a simulation, you can view the waveforms:

```bash
gtkwave output/simple_core_sim/sim.vcd
```

## Analysis Scripts

The environment includes custom Python scripts for analyzing simulation and synthesis results.

### Available Scripts

- **Performance Analysis**: Analyzes execution time and CPI
- **Power Analysis**: Estimates power consumption
- **Area Analysis**: Analyzes gate count and utilization
- **Visualization**: Creates charts and graphs

### Usage

```bash
python build/flows/analysis_flow.py --config build/configs/simple_core_test.yaml
```

## Flow Orchestration Tools

The environment includes tools for orchestrating the entire design flow.

### Main Study Flow

The main study flow coordinates all other flows:

```bash
python build/flows/main_study_flow.py --config build/configs/simple_core_test.yaml --flow=software,simulation,synthesis,analysis
```

### Configuration Utilities

Utilities for loading and validating configurations:

```python
from build.flows.utils.config import load_config

config = load_config("build/configs/simple_core_test.yaml")
```

## Infrastructure Tools

Tools for running flows in cloud or Kubernetes environments.

### Kubernetes

Configuration files for Kubernetes deployment:

```
build/infrastructure/kubernetes/
├── config.yaml
└── job.yaml
```

### Terraform

Terraform scripts for cloud deployment:

```
build/infrastructure/terraform/
```

### Nix

Nix shell for reproducible development environment:

```
build/infrastructure/nix/
└── shell.nix
```

## Validation Tools

Tools for validating the environment setup and test results.

### Test Framework

The test framework uses pytest:

```bash
# Run all tests
pytest validate/tests/

# Run specific tests
pytest validate/tests/test_dependencies.py
```

### Regression Tools

Tools for running regression tests:

```bash
python validate/tools/regression.py
```

## Integration with VS Code

The environment can be integrated with Visual Studio Code for a better development experience.

### Recommended Extensions

- C/C++ Extension
- Python Extension
- Verilog/SystemVerilog Extension
- Bazel Extension

### Debugging

VS Code launch configurations for debugging:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Software Flow",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/build/flows/software_flow.py",
      "args": ["--config", "build/configs/simple_core_test.yaml"],
      "console": "integratedTerminal"
    }
  ]
}
```
