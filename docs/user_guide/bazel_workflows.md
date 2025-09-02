# Bazel Workflows and Stages

This guide explains how to use Bazel for building and running the RISC-V Silicon Design Environment workflows.

## Introduction

The RISC-V SDE uses Bazel as its primary build system to ensure reproducible builds and efficient dependency management. The `run_with_bazel.sh` script provides a convenient wrapper around Bazel commands to execute various workflows.

## Basic Usage

To run the basic workflow:

```bash
./run_with_bazel.sh
```

By default, this runs only the software flow (building RISC-V programs).

## Command-Line Options

The `run_with_bazel.sh` script supports several options:

```bash
./run_with_bazel.sh --help
```

Key options include:

| Option | Description |
|--------|-------------|
| `--flows=FLOWS` | Comma-separated list of flows to run (software,simulation,analysis) |
| `--core=CORE` | The core to simulate (simple_core, picorv32) |
| `--config=FILE` | Configuration file to use |
| `--clean` | Clean build artifacts before running |
| `--output-dir=DIR` | Directory to store outputs (default: output) |
| `--build-docs` | Build documentation |

## Workflow Stages

The RISC-V SDE is organized into several workflow stages, each handling a specific aspect of the design and verification process:

### 1. Software Flow

The software flow compiles RISC-V programs for execution on the cores:

```bash
./run_with_bazel.sh --flows=software
```

This stage:
- Compiles the specified RISC-V applications (e.g., hello-world)
- Generates binary and hex files for simulation
- Uses the RISC-V GCC toolchain via Bazel rules

Key Bazel targets:
- `//design/software/hello-world:executable`

### 2. Simulation Flow

The simulation flow runs RTL simulations of the RISC-V cores:

```bash
./run_with_bazel.sh --flows=simulation --core=simple_core
```

This stage:
- Sets up the simulation environment
- Runs the core simulation with the compiled software
- Generates waveforms and simulation logs

Key Bazel targets:
- `//validate/simulations:simple_core_simulation`
- `//validate/simulations:picorv32_simulation`

### 3. Analysis Flow

The analysis flow processes simulation results to extract metrics:

```bash
./run_with_bazel.sh --flows=analysis
```

This stage (when fully implemented):
- Analyzes simulation logs
- Extracts performance metrics
- Generates reports

### 4. Documentation Flow

To build the documentation:

```bash
./run_with_bazel.sh --build-docs
```

This uses Sphinx to generate HTML documentation.

## Combined Workflows

You can combine multiple flows in a single command:

```bash
./run_with_bazel.sh --flows=software,simulation --core=simple_core
```

This runs both the software compilation and simulation flows for the specified core.

## Customizing Configurations

Each flow can be customized using configuration files:

```bash
./run_with_bazel.sh --flows=software --config=build/configs/custom_config.yaml
```

Configuration files specify:
- Cores to use
- Benchmarks to run
- Simulation parameters
- Output directories

## Bazel Target Structure

The key Bazel targets in the repository are organized as follows:

- `//:orchestration` - Main orchestration target
- `//design/software/...` - RISC-V software applications
- `//design/hardware/rtl/...` - RTL core designs
- `//validate/simulations/...` - Simulation targets
- `//docs/...` - Documentation targets

## Working with Bazel Directly

You can also use Bazel commands directly for more control:

```bash
# Build a specific target
bazel build //design/software/hello-world:executable

# Run a specific binary
bazel run //validate/simulations:simple_core_simulation

# Build all software targets
bazel build //design/software/...

# Clean all build artifacts
bazel clean
```

## Troubleshooting

If you encounter issues:

1. **Working Directory Problems**: Ensure you're in the root directory of the repository when running the script.

2. **Missing Dependencies**: Check if all required tools (RISC-V toolchain, Python packages) are installed.

3. **Build Failures**: Check logs for specific error messages. The most common issue is missing dependencies.

4. **Simulation Errors**: Verify that the RTL files exist and the core configuration is correct.

## Best Practices

1. Start with just the software flow to verify basic functionality:
   ```bash
   ./run_with_bazel.sh --flows=software
   ```

2. Run with clean builds when making significant changes:
   ```bash
   ./run_with_bazel.sh --clean --flows=software
   ```

3. Use explicit configuration files for reproducible results:
   ```bash
   ./run_with_bazel.sh --config=build/configs/simple_core_test.yaml
   ```

4. Check build artifacts in the output directory after each run.
