# Configuration

The RISC-V Silicon Design Environment uses configuration files to control various aspects of the design, simulation, and analysis flows. This document explains how to create and customize configuration files for your specific needs.

## Configuration File Format

Configuration files use YAML format, which provides a human-readable structure that is easy to edit and understand. The basic structure includes:

- Core selection
- Benchmark selection
- Core-specific configuration
- Output directory specification

## Default Configuration

The default configuration file is located at `build/configs/simple_core_test.yaml`:

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

## Configuration Sections

### Cores

The `cores` section lists the RISC-V cores to use in the flow:

```yaml
cores:
  - simple_core
  - picorv32
```

Available cores include:
- `simple_core`: A simple RISC-V core implementation
- `picorv32`: The PicoRV32 RISC-V implementation

### Benchmarks

The `benchmarks` section lists the software benchmarks to compile and run:

```yaml
benchmarks:
  - hello-world
  - matrix_mult
  - fft
  - crypto
```

### Core Configuration

The `cores_config` section provides specific configuration for each core:

```yaml
cores_config:
  simple_core:
    simulator: verilator
    options:
      trace: true
      max_cycles: 10000
      dump_start: 0
      dump_stop: 1000000
    synthesis:
      target_frequency: 100  # MHz
      optimization: area     # area or speed
  picorv32:
    simulator: verilator
    options:
      trace: true
      max_cycles: 20000
```

#### Simulator Options

Common simulator options include:

| Option | Description | Default |
|--------|-------------|---------|
| `trace` | Enable waveform tracing | `true` |
| `max_cycles` | Maximum simulation cycles | `10000` |
| `dump_start` | Cycle to start tracing | `0` |
| `dump_stop` | Cycle to stop tracing | `1000000` |
| `timeout` | Simulation timeout in seconds | `300` |

#### Synthesis Options

Common synthesis options include:

| Option | Description | Default |
|--------|-------------|---------|
| `target_frequency` | Target clock frequency in MHz | `100` |
| `optimization` | Optimization target | `area` |
| `effort` | Synthesis effort level | `medium` |
| `technology` | Target technology node | `skywater130` |

### Output Directory

The `output_dir` specifies where simulation and synthesis results will be stored:

```yaml
output_dir: output/simple_core_test
```

## Using Configuration Files

### Command Line

Configuration files can be specified on the command line:

```bash
# Using the wrapper script
./run_simulation.py --config build/configs/simple_core_test.yaml

# Using specific flow scripts
python build/flows/simulation_flow.py --config build/configs/simple_core_test.yaml
```

### Creating Custom Configurations

To create a custom configuration:

1. Copy an existing configuration file
   ```bash
   cp build/configs/simple_core_test.yaml build/configs/my_custom_config.yaml
   ```

2. Edit the new configuration file
   ```bash
   vim build/configs/my_custom_config.yaml
   ```

3. Run with your custom configuration
   ```bash
   ./run_simulation.py --config build/configs/my_custom_config.yaml
   ```

## Configuration Schema

The full configuration schema includes the following top-level sections:

```yaml
# Core selection
cores: [list of cores]

# Benchmark selection
benchmarks: [list of benchmarks]

# Core-specific configuration
cores_config:
  core_name:
    simulator: [simulator name]
    options: [simulator options]
    synthesis: [synthesis options]
    
# Output directory-2
output_dir: [output directory path]

# Optional global settings
global:
  parallel: [true/false]
  log_level: [debug/info/warning/error]
```

## Configuration Hierarchy

Configuration is loaded in the following order, with later sources overriding earlier ones:

1. Default values in the code
2. Configuration file specified on the command line
3. Command-line arguments that override specific settings
