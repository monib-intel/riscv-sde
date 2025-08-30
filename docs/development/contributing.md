# Contributing Guide

This document provides guidelines for contributing to the RISC-V Silicon Design Environment. We welcome contributions from the community to help improve the project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## Getting Started

1. **Fork the Repository**: Start by forking the repository on GitHub.
2. **Clone Your Fork**: Clone your fork to your local machine.
   ```bash
   git clone https://github.com/your-username/silicon-design-environment.git
   cd silicon-design-environment
   ```
3. **Set Up Development Environment**: Follow the [Installation Guide](../getting_started/installation.md) to set up your development environment.
4. **Create a Branch**: Create a branch for your contribution.
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Contribution Workflow

### 1. Identify an Area to Contribute

You can contribute in several ways:
- Fix bugs
- Add new features
- Improve documentation
- Add new cores or benchmarks
- Enhance build system

Check the GitHub issues for current tasks or create a new issue to discuss your proposed changes.

### 2. Make Your Changes

- Follow the [Project Structure](../user_guide/project_structure.md) guidelines.
- Adhere to the coding standards (see below).
- Write tests for new functionality.
- Update documentation as needed.

### 3. Test Your Changes

Before submitting your changes, ensure all tests pass:

```bash
# Run unit tests
pytest validate/tests/

# Run integration tests
./run_simulation.py --clean --config build/configs/simple_core_test.yaml
```

### 4. Submit a Pull Request

1. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Create a pull request on GitHub.
3. Describe your changes in detail.
4. Link to any relevant issues.

### 5. Code Review

- Maintainers will review your pull request.
- Address any feedback or requested changes.
- Once approved, your changes will be merged.

## Coding Standards

### Python Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
- Use type hints where appropriate.
- Include docstrings for all functions, classes, and modules.
- Use meaningful variable and function names.
- Keep functions focused on a single responsibility.

Example:
```python
def calculate_performance_metrics(simulation_results: dict, config: dict) -> dict:
    """
    Calculate performance metrics from simulation results.
    
    Args:
        simulation_results: Dictionary containing simulation results
        config: Configuration dictionary
        
    Returns:
        Dictionary containing calculated performance metrics
    """
    # Implementation
    return metrics
```

### Verilog Code

- Follow a consistent indentation style (2 or 4 spaces).
- Use meaningful module, signal, and parameter names.
- Include comprehensive comments.
- Add proper port declarations.
- Use parameters for configurable values.

Example:
```verilog
/**
 * Module: alu
 * Description: Arithmetic Logic Unit for RISC-V core
 */
module alu #(
    parameter WIDTH = 32  // Width of the ALU
) (
    input  wire                clk,
    input  wire                reset_n,
    input  wire [WIDTH-1:0]    operand_a,
    input  wire [WIDTH-1:0]    operand_b,
    input  wire [3:0]          operation,
    output reg  [WIDTH-1:0]    result,
    output reg                 zero_flag
);
    // Implementation
endmodule
```

### Bazel Build Files

- Group related targets together.
- Use descriptive target names.
- Include comprehensive visibility declarations.
- Document complex build rules.

Example:
```python
# BUILD file for simulation components

# RTL components
verilog_library(
    name = "simulation_rtl",
    srcs = glob(["*.v"]),
    deps = [
        "//design/hardware/rtl/common:common_rtl",
    ],
    visibility = ["//visibility:public"],
)

# Testbench components
verilog_library(
    name = "testbench",
    srcs = glob(["testbench/*.v"]),
    deps = [
        ":simulation_rtl",
    ],
    visibility = ["//visibility:public"],
)
```

## Documentation Guidelines

- Use Markdown for documentation.
- Include clear explanations and examples.
- Update documentation when you change code.
- Follow the existing documentation structure.

## Adding New Components

### Adding a New Core

1. Create a directory in `design/hardware/rtl/cores/your_core_name/`
2. Add your RTL files
3. Create a `BUILD.bazel` file
4. Add a testbench in `design/hardware/rtl/testbench/`
5. Update flow scripts to support your core
6. Add documentation in `docs/reference/cores.md`

### Adding a New Benchmark

1. Create a directory in `design/software/your_benchmark_name/`
2. Add your source files
3. Create a `BUILD.bazel` file
4. Update flow scripts to recognize your benchmark
5. Add documentation in `docs/reference/benchmarks.md`

## Commit Message Guidelines

- Use clear and descriptive commit messages
- Start with a short summary line (50 characters or less)
- Follow with a blank line and more detailed description
- Reference issues or pull requests where appropriate

Example:
```
Add matrix multiplication benchmark

This commit adds a new benchmark for matrix multiplication with the
following features:
- Configurable matrix size
- Both integer and floating-point versions
- Performance metrics calculation

Fixes #42
```

## Versioning

We follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality
- PATCH version for backwards-compatible bug fixes

## License

By contributing to this project, you agree that your contributions will be licensed under the project's license.

## Questions and Support

If you have questions or need help, you can:
- Open an issue on GitHub
- Contact the maintainers
- Join the project's communication channels (if available)

Thank you for contributing to the RISC-V Silicon Design Environment!
