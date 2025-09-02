# RISC-V Cores

The RISC-V Silicon Design Environment includes several RISC-V core implementations that can be used for simulation, synthesis, and analysis. This document provides details about each available core.

## Overview of Available Cores

| Core Name | ISA | Pipeline Stages | Features | Best For |
|-----------|-----|-----------------|----------|----------|
| SimpleCore | RV32I | 3 | Basic implementation, easily customizable | Learning, simple tests |
| PicoRV32 | RV32IMC | 2-3 | Compact, configurable | Area-optimized designs |

## SimpleCore

SimpleCore is a basic RISC-V implementation that supports the RV32I instruction set. It is designed to be easily understandable and modifiable.

### Architecture-2

SimpleCore uses a 3-stage pipeline:
1. **Fetch**: Fetches instructions from memory
2. **Decode**: Decodes instructions and reads registers
3. **Execute**: Executes instructions and writes results

### Key Features-2

- RV32I instruction set support
- Harvard architecture (separate instruction and data memory)
- Configurable memory sizes
- Simple memory-mapped I/O
- Easily extensible for custom instructions

### Configuration Options-2

In the configuration file (`build/configs/simple_core_test.yaml`):

```yaml
cores_config:
  simple_core:
    simulator: verilator
    options:
      trace: true
      max_cycles: 10000
```

### Performance Characteristics-2

- **Clock Frequency**: ~50-100 MHz (in ASIC implementations)
- **Area**: ~10-20K gates
- **Power**: Low
- **CPI (Cycles Per Instruction)**: ~1.5-2.0

### Source Files-2

The SimpleCore RTL is located in:
```
design/hardware/rtl/cores/simple_core/
```

## PicoRV32

PicoRV32 is a small RISC-V CPU core that implements the RV32IMC instruction set. It's designed to be compact and efficient.

### Architecture

PicoRV32 uses a minimalist design with:
- Single-issue in-order execution
- Configurable pipeline depth (2-3 stages)
- Shared instruction and data memory interface

### Key Features

- RV32IMC instruction set support
- Optional compressed instruction support
- Configurable interrupt controller
- AXI4-Lite interface
- Look-ahead instruction fetch

### Configuration Options

In the configuration file:

```yaml
cores_config:
  picorv32:
    simulator: verilator
    options:
      trace: true
      max_cycles: 20000
    features:
      compressed: true
      multiplier: true
      interrupts: true
```

### Performance Characteristics

- **Clock Frequency**: ~100-150 MHz (in ASIC implementations)
- **Area**: ~15-25K gates
- **Power**: Low
- **CPI (Cycles Per Instruction)**: ~1.2-1.8

### Source Files

The PicoRV32 RTL is located in:
```
design/hardware/rtl/cores/picorv32/
```

## Adding a New Core

To add a new RISC-V core to the environment:

1. Create a new directory in `design/hardware/rtl/cores/`
2. Add your RTL files to the new directory
3. Create a `BUILD.bazel` file for your core
4. Add a testbench in `design/hardware/rtl/testbench/`
5. Update flow scripts to support your core
6. Add configuration options to your YAML files

Example `BUILD.bazel` for a new core:

```python
load("//build/bazel:verilog.bzl", "verilog_library")

verilog_library(
    name = "my_new_core_rtl",
    srcs = glob(["*.v"]),
    deps = [
        "//design/hardware/rtl/common:common_rtl",
    ],
    visibility = ["//visibility:public"],
)
```

## Core Comparison

### Performance

The following table shows performance metrics for the available cores on common benchmarks:

| Core | Dhrystone (DMIPS/MHz) | CoreMark/MHz | Area (kGE) |
|------|----------------------|--------------|------------|
| SimpleCore | 0.8 | 1.2 | 15 |
| PicoRV32 | 1.0 | 1.5 | 20 |

### Feature Comparison

| Feature | SimpleCore | PicoRV32 |
|---------|------------|----------|
| RV32I | ✅ | ✅ |
| RV32M | ❌ | ✅ |
| RV32C | ❌ | ✅ |
| Interrupts | Basic | Configurable |
| Debug | Limited | Full |
| Memory Interface | Simple | AXI4-Lite |
| Pipeline Stages | 3 | 2-3 |

## Core Selection Guide

- **For learning and teaching**: Use SimpleCore for its clarity and simplicity
- **For area-optimized designs**: Use PicoRV32 for its compact implementation
- **For performance**: PicoRV32 generally offers better performance

## Future Cores

Planned additions to the core library include:
- RocketCore (RV64GC)
- BOOM (RV64GC out-of-order)
- CVA6 (RV32/64GC)
