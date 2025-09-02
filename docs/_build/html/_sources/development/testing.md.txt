# Testing

This document describes the testing framework for the RISC-V Silicon Design Environment and provides guidelines for writing and running tests.

## Testing Framework

The project uses pytest for testing. Tests are organized in the `validate/tests/` directory:

```
validate/
├── output/             # Validation outputs
├── tests/              # Test files
│   ├── conftest.py     # PyTest configuration
│   ├── pytest.ini      # PyTest initialization
│   ├── test_basic.py   # Basic tests
│   └── test_dependencies.py # Dependency tests
└── tools/              # Validation tools
    ├── __init__.py
    ├── config.py       # Configuration utilities
    └── regression.py   # Regression test utilities
```

## Test Categories

The testing framework includes several categories of tests:

### 1. Dependency Tests

These tests verify that all required dependencies are installed and properly configured.

Example:
```python
def test_verilator_installed():
    """Test that Verilator is installed and available on the PATH."""
    result = subprocess.run(['verilator', '--version'], 
                           capture_output=True, text=True)
    assert result.returncode == 0, "Verilator is not installed"
    assert "Verilator" in result.stdout, "Verilator version string not found"
```

### 2. Configuration Tests

These tests verify that configuration loading works properly.

Example:
```python
def test_config_loading():
    """Test that configuration files can be loaded correctly."""
    config = load_config('build/configs/simple_core_test.yaml')
    assert 'cores' in config, "Missing 'cores' section in config"
    assert 'benchmarks' in config, "Missing 'benchmarks' section in config"
```

### 3. Project Structure Tests

These tests verify that the project structure is as expected.

Example:
```python
def test_directory_structure():
    """Test that key directories exist."""
    assert os.path.isdir('design'), "Missing 'design' directory"
    assert os.path.isdir('build'), "Missing 'build' directory"
    assert os.path.isdir('validate'), "Missing 'validate' directory"
```

### 4. Flow Tests

These tests verify that the flows work properly.

Example:
```python
def test_software_flow():
    """Test that software flow compiles correctly."""
    config = load_config('build/configs/simple_core_test.yaml')
    result = run_software_flow(config)
    assert result, "Software flow failed"
    assert os.path.exists('output/hello_world.hex'), "Output file not created"
```

### 5. Integration Tests

These tests verify that different components work together correctly.

Example:
```python
def test_end_to_end():
    """Test end-to-end flow from software compilation to simulation."""
    # Run the simulation using the wrapper script
    result = subprocess.run(['./run_simulation.py', '--clean'], 
                           capture_output=True, text=True)
    assert result.returncode == 0, "Simulation failed"
    assert os.path.exists('output/simple_core_sim/sim.vcd'), "VCD file not created"
```

## Running Tests

### Running All Tests

To run all tests:

```bash
# From the project root
pytest validate/tests/

# For more verbosity
pytest -v validate/tests/
```

### Running Specific Tests

To run a specific test file:

```bash
pytest validate/tests/test_dependencies.py
```

To run a specific test function:

```bash
pytest validate/tests/test_dependencies.py::test_verilator_installed
```

### Test Configuration

Test configuration is defined in `validate/tests/pytest.ini`:

```ini
[pytest]
testpaths = validate/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

## Writing Tests

### Test File Structure

Test files should follow this structure:

```python
"""
Test module for [component].
"""

import os
import pytest
import subprocess

# Import components to test
from build.flows.utils.config import load_config

def test_something():
    """Test description."""
    # Test implementation
    assert condition, "Failure message"
```

### Best Practices for Tests

1. **Isolation**: Each test should be independent and not rely on the state from other tests.
2. **Clear Purpose**: Each test should have a clear purpose, testing one specific thing.
3. **Descriptive Names**: Use descriptive test names that indicate what is being tested.
4. **Comments**: Include comments to explain complex test logic.
5. **Fixtures**: Use pytest fixtures for common setup and teardown.
6. **Parameterization**: Use parameterized tests for testing multiple inputs.

### Fixtures

Fixtures provide a way to set up preconditions for tests:

```python
@pytest.fixture
def simple_config():
    """Fixture that provides a basic configuration."""
    return load_config('build/configs/simple_core_test.yaml')

def test_with_config(simple_config):
    """Test that uses the simple_config fixture."""
    assert 'cores' in simple_config
```

### Parameterized Tests

Parameterized tests allow testing multiple inputs:

```python
@pytest.mark.parametrize("core_name", ["simple_core", "picorv32"])
def test_core_configuration(core_name, simple_config):
    """Test that configuration for different cores works."""
    assert core_name in simple_config['cores'] or core_name in simple_config['cores_config']
```

## Continuous Integration

The project uses continuous integration to automatically run tests on every push and pull request.

### CI Configuration

CI is configured to:
1. Install dependencies
2. Build the project
3. Run tests
4. Report results

### Running CI Locally

You can simulate the CI environment locally:

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest validate/tests/
```

## Regression Testing

The project includes regression testing tools in `validate/tools/regression.py`.

### Running Regression Tests

```bash
python validate/tools/regression.py
```

This will:
1. Run all tests
2. Compare results with previous runs
3. Report any regressions

### Regression Test Configuration

Regression tests can be configured in a YAML file:

```yaml
regression_tests:
  - name: basic
    test_path: validate/tests/test_basic.py
  - name: dependencies
    test_path: validate/tests/test_dependencies.py
  - name: software_flow
    test_path: validate/tests/test_flows.py::test_software_flow
```

## Performance Testing

Performance tests measure the execution time, resource usage, and other performance metrics.

### Writing Performance Tests

```python
def test_simulation_performance():
    """Test simulation performance."""
    start_time = time.time()
    # Run simulation
    result = subprocess.run(['./run_simulation.py'], 
                           capture_output=True, text=True)
    end_time = time.time()
    
    # Check that simulation completes within the expected time
    assert end_time - start_time < 60, "Simulation took too long"
```

### Benchmarking

For more detailed benchmarking:

```python
@pytest.mark.benchmark
def test_benchmark_simulation(benchmark):
    """Benchmark simulation performance."""
    benchmark(run_simulation_with_default_config)
```

## Coverage

The project uses coverage.py to measure test coverage.

### Running Tests with Coverage

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage
pytest --cov=build validate/tests/

# Generate coverage report
pytest --cov=build --cov-report=html validate/tests/
```

### Coverage Goals

The project aims for:
- 80% line coverage
- 70% branch coverage
- Coverage of all critical components

## Adding New Tests

When adding new functionality, also add corresponding tests:

1. Create a new test file or add to an existing file
2. Write tests for the new functionality
3. Ensure tests are isolated and independent
4. Update documentation if necessary
