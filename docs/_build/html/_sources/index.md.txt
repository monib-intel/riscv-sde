# RISC-V Silicon Design Environment

```{toctree}
:maxdepth: 2
:caption: Getting Started
:hidden:

getting_started/installation
getting_started/quickstart
```

```{toctree}
:maxdepth: 2
:caption: User Guide
:hidden:

user_guide/project_structure
user_guide/configuration
user_guide/workflows
```

```{toctree}
:maxdepth: 2
:caption: Reference
:hidden:

reference/cores
reference/benchmarks
reference/tools
reference/api
```

```{toctree}
:maxdepth: 2
:caption: Development
:hidden:

development/contributing
development/testing
development/ci_cd
```

## Welcome to the RISC-V Silicon Design Environment

The RISC-V Silicon Design Environment is a comprehensive toolset for designing, simulating, and analyzing RISC-V based silicon designs. This framework integrates RTL design, simulation, synthesis, and analysis in a unified workflow.

![Architecture Overview](/_static/architecture_diagram.png)

## Key Features

- **Modular RISC-V Cores**: Pre-integrated RISC-V processor cores with customizable configurations
- **End-to-End Flows**: Complete flows from RTL to gate-level simulation and analysis
- **Bazel Integration**: Consistent and reproducible build system for both hardware and software components
- **Benchmark Suite**: Ready-to-use software benchmarks for performance analysis
- **Analysis Tools**: Powerful tools for power, performance, and area (PPA) analysis
- **CI/CD Ready**: Ready for integration with continuous integration pipelines

## Quick Links

- [Installation Guide](getting_started/installation.md)
- [Quick Start Tutorial](getting_started/quickstart.md)
- [Project Structure](user_guide/project_structure.md)
- [Available Cores](reference/cores.md)
- [Benchmarks](reference/benchmarks.md)
- [Contributing](development/contributing.md)

## Indices and Tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
