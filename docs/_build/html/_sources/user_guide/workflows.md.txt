# Workflows

The RISC-V Silicon Design Environment provides several predefined workflows to handle different aspects of the design and verification process. This document describes the available workflows and how to use them.

## Overview

The environment uses Prefect for workflow orchestration and Bazel for build management. This combination provides:

1. **Reproducible Builds**: Bazel ensures consistent and reproducible builds
2. **Efficient Orchestration**: Prefect manages dependencies between tasks and caching
3. **Observability**: Prefect provides monitoring and visualization of workflow execution
4. **Scalability**: The workflows can be run locally or distributed across multiple machines

## Available Workflows

The environment includes the following core workflows:

1. **Software Flow**: Compiles RISC-V programs for execution on cores
2. **Simulation Flow**: Simulates RTL designs running the compiled programs
3. **Synthesis Flow**: Performs logic synthesis for implementation
4. **Verification Flow**: Verifies correctness of designs
5. **Analysis Flow**: Analyzes results for power, performance, and area metrics

## Software Flow

The software flow compiles C/C++/Rust programs for RISC-V targets.

### Running the Software Flow

```bash
# Using the orchestration script-7-6-5-4-3-2
./run_with_bazel.sh --flows=software

# Using Bazel directly-7-6-5-4-3-2
bazel run //build/flows:software_flow_bin -- --config=build/configs/simple_core_test.yaml
```

### Flow Stages-5-4-3-2

1. **Source Selection**: Identifies source files based on the configuration
2. **Compilation**: Compiles sources using RISC-V GCC/LLVM toolchain
3. **Linking**: Links object files into an executable
4. **Binary Generation**: Creates binary and memory images for simulation

### Customization-3-2

You can customize the software flow by modifying:
- Compiler flags in the configuration
- Memory map in `memory.x` files
- Build rules in `BUILD.bazel` files

## Simulation Flow

The simulation flow runs RTL designs with the compiled software.

### Running the Simulation Flow

```bash
# Using the orchestration script
./run_with_bazel.sh --flows=simulation

# Using Bazel directly
bazel run //build/flows:simulation_flow_bin -- --config=build/configs/simple_core_test.yaml
```

### Flow Stages

1. **RTL Compilation**: Compiles Verilog/SystemVerilog into simulator model
2. **Testbench Setup**: Sets up testbench environment
3. **Simulation**: Runs the simulation with compiled software
4. **Result Collection**: Collects and stores simulation results

### Customization

Simulation parameters can be adjusted in the configuration file:
- Simulation time
- Trace options
- Debugging settings

## Synthesis Flow

The synthesis flow performs logic synthesis for ASIC or FPGA implementation.

### Running the Synthesis Flow

```bash
# Using the orchestration script
./run_with_bazel.sh --flows=synthesis

# Using Bazel directly
bazel run //build/flows:synthesis_flow_bin -- --config=build/configs/simple_core_test.yaml
```

### Flow Stages

1. **RTL Elaboration**: Elaborates the RTL design
2. **Constraint Application**: Applies timing and area constraints
3. **Logic Synthesis**: Performs technology mapping
4. **Reporting**: Generates area, timing, and power reports

### Customization

Synthesis parameters can be configured:
- Target technology
- Optimization goals (area/speed)
- Clock frequency

## Verification Flow

The verification flow ensures correctness of the design.

### Running the Verification Flow

```bash
# Using the orchestration script
./run_with_bazel.sh --flows=verification

# Using Bazel directly
bazel run //build/flows:verification_flow_bin -- --config=build/configs/simple_core_test.yaml
```

### Flow Stages

1. **Formal Verification**: Applies formal verification techniques
2. **Directed Testing**: Runs directed test cases
3. **Compliance Testing**: Verifies RISC-V ISA compliance
4. **Reporting**: Generates coverage and verification reports

## Analysis Flow

The analysis flow examines results from simulation and synthesis.

### Running the Analysis Flow

```bash
# Using the orchestration script
./run_with_bazel.sh --flows=analysis

# Using Bazel directly
bazel run //build/flows:analysis_flow_bin -- --config=build/configs/simple_core_test.yaml
```

### Flow Stages

1. **Data Collection**: Gathers simulation and synthesis results
2. **Metrics Calculation**: Computes performance, power, and area metrics
3. **Visualization**: Generates charts and graphs
4. **Report Generation**: Creates detailed analysis reports

## Combined Flows

You can run multiple flows together using the main study flow.

### Running Combined Flows

```bash
# Using the orchestration script
./run_with_bazel.sh --flows=software,simulation,analysis

# Using Bazel directly
bazel run //:orchestration -- --flows=software,simulation,analysis
```

Available flow combinations:
- `software,simulation`: Compile and simulate
- `software,simulation,analysis`: Compile, simulate, and analyze
- `software,simulation,synthesis,analysis`: Complete flow

## Documentation Flow

The environment also includes a documentation flow to build the documentation:

```bash
# Using the orchestration script
./run_with_bazel.sh --build-docs

# Using Bazel directly
bazel build //docs:docs_html
```

## Prefect Orchestration

The environment uses Prefect for workflow orchestration. Prefect provides several benefits:

1. **Task Caching**: Results of tasks are cached to avoid redundant work
2. **Dependency Management**: Tasks only run when their dependencies are satisfied
3. **Parallel Execution**: Independent tasks can run in parallel
4. **Failure Handling**: Tasks can be retried or resumed after failures
5. **Observability**: Task execution can be monitored and visualized

### Prefect UI

If you have Prefect installed and configured, you can start the Prefect UI to monitor workflows:

```bash
prefect server start
```

Then visit [http://localhost:4200](http://localhost:4200) to access the UI.

### Prefect Flow Structure

The orchestration is defined in `build/scripts/orchestration.py` and includes the following flows:

1. **Software Flow**: Compiles RISC-V programs
2. **Simulation Flow**: Simulates RTL designs
3. **Analysis Flow**: Analyzes simulation results
4. **Main Flow**: Orchestrates all sub-flows

## Custom Flows

You can create custom flows by:

1. Creating a new Python file in the `build/flows` directory
2. Importing and combining existing flow components
3. Adding your custom logic

Example of a custom flow:

```python
#!/usr/bin/env python3
"""
Custom flow that combines simulation with specialized analysis.
"""

import argparse
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flows.software_flow import run_software_flow
from flows.simulation_flow import run_simulation_flow
from flows.utils.config import load_config

def run_custom_flow(config_path):
    """Run the custom flow with the given configuration."""
    config = load_config(config_path)
    
    # Run standard flows
    run_software_flow(config)
    run_simulation_flow(config)
    
    # Add custom analysis
    print("Running custom analysis...")
    # Your custom analysis code here
    
    print("Custom flow completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run custom RISC-V flow")
    parser.add_argument("--config", default="build/configs/simple_core_test.yaml",
                        help="Configuration file to use")
    args = parser.parse_args()
    
    run_custom_flow(args.config)
```

## Workflow Integration

The workflows can be integrated with:

- **Continuous Integration**: Through GitHub Actions or Jenkins
- **Cloud Execution**: Using the infrastructure in `build/infrastructure/`
- **Local Development**: Using the wrapper scripts in the repository root
