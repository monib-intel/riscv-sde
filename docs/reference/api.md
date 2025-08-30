# API Reference

The RISC-V Silicon Design Environment provides Python APIs for interacting with the various flows and components. This document serves as a reference for these APIs.

## Flow APIs

### Software Flow API

The software flow API provides functions for compiling RISC-V software.

```python
from build.flows.software_flow import run_software_flow, compile_benchmark

# Run the entire software flow
run_software_flow(config)

# Compile a specific benchmark
compile_benchmark(benchmark_name, config, output_dir)
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `run_software_flow(config)` | Runs the complete software flow | `config`: Configuration dictionary |
| `compile_benchmark(benchmark_name, config, output_dir)` | Compiles a specific benchmark | `benchmark_name`: Name of benchmark<br>`config`: Configuration dictionary<br>`output_dir`: Output directory |
| `generate_hex(elf_file, hex_file)` | Generates a hex file from an ELF file | `elf_file`: Input ELF file<br>`hex_file`: Output hex file |

### Simulation Flow API

The simulation flow API provides functions for simulating RISC-V cores.

```python
from build.flows.simulation_flow import run_simulation_flow, simulate_core

# Run the entire simulation flow
run_simulation_flow(config)

# Simulate a specific core
simulate_core(core_name, program_hex, config, output_dir)
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `run_simulation_flow(config)` | Runs the complete simulation flow | `config`: Configuration dictionary |
| `simulate_core(core_name, program_hex, config, output_dir)` | Simulates a specific core | `core_name`: Name of core<br>`program_hex`: Program hex file<br>`config`: Configuration dictionary<br>`output_dir`: Output directory |
| `parse_simulation_results(output_dir)` | Parses simulation results | `output_dir`: Simulation output directory |

### Synthesis Flow API

The synthesis flow API provides functions for synthesizing RISC-V cores.

```python
from build.flows.synthesis_flow import run_synthesis_flow, synthesize_core

# Run the entire synthesis flow
run_synthesis_flow(config)

# Synthesize a specific core
synthesize_core(core_name, config, output_dir)
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `run_synthesis_flow(config)` | Runs the complete synthesis flow | `config`: Configuration dictionary |
| `synthesize_core(core_name, config, output_dir)` | Synthesizes a specific core | `core_name`: Name of core<br>`config`: Configuration dictionary<br>`output_dir`: Output directory |
| `parse_synthesis_results(output_dir)` | Parses synthesis results | `output_dir`: Synthesis output directory |

### Analysis Flow API

The analysis flow API provides functions for analyzing results.

```python
from build.flows.analysis_flow import run_analysis_flow, analyze_simulation

# Run the entire analysis flow
run_analysis_flow(config)

# Analyze simulation results
analyze_simulation(simulation_dir, config)
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `run_analysis_flow(config)` | Runs the complete analysis flow | `config`: Configuration dictionary |
| `analyze_simulation(simulation_dir, config)` | Analyzes simulation results | `simulation_dir`: Simulation directory<br>`config`: Configuration dictionary |
| `analyze_synthesis(synthesis_dir, config)` | Analyzes synthesis results | `synthesis_dir`: Synthesis directory<br>`config`: Configuration dictionary |
| `generate_report(results, output_dir)` | Generates an analysis report | `results`: Analysis results<br>`output_dir`: Output directory |

### Main Study Flow API

The main study flow API provides functions for orchestrating all flows.

```python
from build.flows.main_study_flow import run_main_study_flow

# Run the main study flow
run_main_study_flow(config, flows=['software', 'simulation', 'analysis'])
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `run_main_study_flow(config, flows)` | Runs the main study flow | `config`: Configuration dictionary<br>`flows`: List of flows to run |

## Utility APIs

### Configuration Utilities

The configuration utilities provide functions for loading and validating configurations.

```python
from build.flows.utils.config import load_config, validate_config

# Load a configuration from a file
config = load_config('build/configs/simple_core_test.yaml')

# Validate a configuration
validate_config(config)
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `load_config(config_path)` | Loads a configuration from a file | `config_path`: Path to configuration file |
| `validate_config(config)` | Validates a configuration | `config`: Configuration dictionary |
| `merge_configs(base_config, override_config)` | Merges two configurations | `base_config`: Base configuration<br>`override_config`: Override configuration |

### Logging Utilities

The logging utilities provide functions for logging.

```python
from build.flows.utils.logging import setup_logging, get_logger

# Set up logging
setup_logging(log_level='INFO', log_file='flow.log')

# Get a logger
logger = get_logger('software_flow')
logger.info('Compiling benchmark...')
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `setup_logging(log_level, log_file)` | Sets up logging | `log_level`: Logging level<br>`log_file`: Log file path |
| `get_logger(name)` | Gets a logger | `name`: Logger name |

### Visualization Utilities

The visualization utilities provide functions for creating charts and graphs.

```python
from build.flows.utils.visualization import plot_performance, plot_area

# Plot performance metrics
plot_performance(results, output_file='performance.png')

# Plot area metrics
plot_area(results, output_file='area.png')
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `plot_performance(results, output_file)` | Plots performance metrics | `results`: Performance results<br>`output_file`: Output file path |
| `plot_area(results, output_file)` | Plots area metrics | `results`: Area results<br>`output_file`: Output file path |
| `plot_power(results, output_file)` | Plots power metrics | `results`: Power results<br>`output_file`: Output file path |
| `plot_comparison(results, metric, output_file)` | Plots a comparison of metrics | `results`: Results to compare<br>`metric`: Metric to compare<br>`output_file`: Output file path |

### Bazel Utilities

The Bazel utilities provide functions for interacting with Bazel.

```python
from build.flows.utils.bazel import run_bazel_build, run_bazel_test

# Run a Bazel build
run_bazel_build('//design/software/hello-world:executable')

# Run a Bazel test
run_bazel_test('//validate/tests:test_dependencies')
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `run_bazel_build(target)` | Runs a Bazel build | `target`: Bazel target |
| `run_bazel_test(target)` | Runs a Bazel test | `target`: Bazel target |
| `get_bazel_output_path(target)` | Gets the output path for a Bazel target | `target`: Bazel target |

### Tool Utilities

The tool utilities provide functions for interacting with external tools.

```python
from build.flows.utils.tools import run_verilator, run_yosys

# Run Verilator
run_verilator(rtl_files, top_module, output_dir, verilator_args)

# Run Yosys
run_yosys(rtl_files, top_module, output_dir, yosys_script)
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `run_verilator(rtl_files, top_module, output_dir, verilator_args)` | Runs Verilator | `rtl_files`: RTL files<br>`top_module`: Top module name<br>`output_dir`: Output directory<br>`verilator_args`: Verilator arguments |
| `run_yosys(rtl_files, top_module, output_dir, yosys_script)` | Runs Yosys | `rtl_files`: RTL files<br>`top_module`: Top module name<br>`output_dir`: Output directory<br>`yosys_script`: Yosys script |
| `run_openroad(config_file, output_dir)` | Runs OpenROAD | `config_file`: Configuration file<br>`output_dir`: Output directory |

## Core Configuration API

The core configuration API provides functions for configuring cores.

```python
from build.flows.utils.core_config import get_core_config, configure_core

# Get the configuration for a core
core_config = get_core_config('simple_core', config)

# Configure a core
configure_core('simple_core', core_config, output_dir)
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `get_core_config(core_name, config)` | Gets the configuration for a core | `core_name`: Name of core<br>`config`: Configuration dictionary |
| `configure_core(core_name, core_config, output_dir)` | Configures a core | `core_name`: Name of core<br>`core_config`: Core configuration<br>`output_dir`: Output directory |

## Benchmark Configuration API

The benchmark configuration API provides functions for configuring benchmarks.

```python
from build.flows.utils.benchmark_config import get_benchmark_config, configure_benchmark

# Get the configuration for a benchmark
benchmark_config = get_benchmark_config('hello-world', config)

# Configure a benchmark
configure_benchmark('hello-world', benchmark_config, output_dir)
```

#### Key Functions

| Function | Description | Parameters |
|----------|-------------|------------|
| `get_benchmark_config(benchmark_name, config)` | Gets the configuration for a benchmark | `benchmark_name`: Name of benchmark<br>`config`: Configuration dictionary |
| `configure_benchmark(benchmark_name, benchmark_config, output_dir)` | Configures a benchmark | `benchmark_name`: Name of benchmark<br>`benchmark_config`: Benchmark configuration<br>`output_dir`: Output directory |
