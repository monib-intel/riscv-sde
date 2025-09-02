# Benchmarks

The RISC-V Silicon Design Environment includes a variety of software benchmarks that can be used to evaluate the performance of RISC-V cores. This document describes the available benchmarks and how to use them.

## Available Benchmarks

| Benchmark | Category | Description | Metrics |
|-----------|----------|-------------|---------|
| hello-world | Basic | Simple "Hello World" program | Execution time |
| matrix_mult | Computation | Matrix multiplication | FLOPS, Execution time |
| fft | DSP | Fast Fourier Transform | FLOPS, Execution time |
| crypto | Security | Cryptographic algorithms | Throughput |

## Hello World

The "Hello World" benchmark is a simple program that prints "Hello, World!" to the console. It serves as a basic test to verify that the core is functioning correctly.

### Source Files-4-3-2

```
design/software/hello-world/
├── BUILD.bazel
├── Cargo.lock
├── Cargo.toml
├── generate_hex.csh
├── make_hex.py
├── Makefile
├── memory.x
├── project.json
├── test_config.json
└── src/
```

### Building-4-3-2

```bash
# Using Bazel
bazel build //design/software/hello-world:executable

# Using Make
cd design/software/hello-world
make
```

### Running-4-3-2

```bash
# Using the simulation wrapper
./run_simulation.py --config build/configs/simple_core_test.yaml
```

### Expected Output

```
Hello, World!
Execution completed successfully.
```

## Matrix Multiplication

The matrix multiplication benchmark performs multiplication of two matrices and measures the execution time.

### Source Files

```
design/software/matrix_mult/
└── matrix_mult.c
```

### Parameters-2

The benchmark can be configured with different matrix sizes:

- Small: 16x16 matrices
- Medium: 32x32 matrices
- Large: 64x64 matrices

### Building

```bash
bazel build //design/software/matrix_mult:executable
```

### Running

```bash
# Create a custom configuration-3-2
cp build/configs/simple_core_test.yaml build/configs/matrix_test.yaml

# Edit the configuration-4-3-2
# Set benchmarks: [matrix_mult]

# Run the simulation-4-3-2
./run_simulation.py --config build/configs/matrix_test.yaml
```

### Metrics-3-2

- **Execution Time**: Time to complete the multiplication
- **Cycles per Operation**: Clock cycles per multiplication operation
- **Memory Access Patterns**: Analysis of memory access behavior

## Fast Fourier Transform (FFT)

The FFT benchmark implements a Fast Fourier Transform algorithm.

### Source Files

```
design/software/fft/
└── fft.c
```

### Parameters

- FFT size: 128, 256, 512, or 1024 points
- Data type: fixed-point or floating-point (if supported)

### Building

```bash
bazel build //design/software/fft:executable
```

### Running

```bash
# Create a custom configuration
cp build/configs/simple_core_test.yaml build/configs/fft_test.yaml

# Edit the configuration
# Set benchmarks: [fft]

# Run the simulation
./run_simulation.py --config build/configs/fft_test.yaml
```

### Metrics

- **Execution Time**: Time to complete the FFT
- **Accuracy**: Comparison with reference results
- **Memory Usage**: Stack and heap memory usage

## Cryptography

The cryptography benchmark implements various cryptographic algorithms.

### Source Files

```
design/software/crypto/
└── sha256.c
```

Currently, SHA-256 is implemented, with plans to add:
- AES
- RSA
- ECC

### Building

```bash
bazel build //design/software/crypto:executable
```

### Running

```bash
# Create a custom configuration
cp build/configs/simple_core_test.yaml build/configs/crypto_test.yaml

# Edit the configuration
# Set benchmarks: [crypto]

# Run the simulation
./run_simulation.py --config build/configs/crypto_test.yaml
```

### Metrics

- **Throughput**: Bytes processed per second
- **Latency**: Time to process a single block
- **Code Size**: Size of the compiled algorithm

## Adding a New Benchmark

To add a new benchmark:

1. Create a new directory in `design/software/`
2. Add your source files (C, C++, or Rust)
3. Create a `BUILD.bazel` file
4. Update the flow scripts to recognize your benchmark
5. Update the configuration files to include your benchmark

Example `BUILD.bazel` for a new benchmark:

```python
load("//build/bazel:riscv.bzl", "riscv_binary")

riscv_binary(
    name = "executable",
    srcs = ["my_benchmark.c"],
    deps = [
        "//design/software/common:common_lib",
    ],
    visibility = ["//visibility:public"],
)
```

## Benchmark Suite

For comprehensive performance analysis, you can run the complete benchmark suite:

```bash
# Create a configuration with all benchmarks
cp build/configs/simple_core_test.yaml build/configs/full_suite.yaml

# Edit the configuration
# Set benchmarks: [hello-world, matrix_mult, fft, crypto]

# Run the simulation
./run_simulation.py --config build/configs/full_suite.yaml
```

## Analysis Tools

The environment includes tools for analyzing benchmark results:

```bash
# Run analysis on benchmark results
python build/flows/analysis_flow.py --config build/configs/full_suite.yaml
```

The analysis will generate:
- Performance charts
- Execution time comparisons
- Memory usage statistics
- Instruction mix analysis
