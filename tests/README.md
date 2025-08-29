# Testing the Silicon Design Environment

This directory contains tests to verify that the silicon design environment is set up correctly.

## Running Tests

To run all tests:

```bash
# From the project root
pytest tests/

# Or for more verbosity
pytest -v tests/
```

To run a specific test file:

```bash
pytest tests/test_dependencies.py
```

## Test Categories

1. **Dependency Tests** - Verify that all required dependencies are installed and properly configured
2. **Configuration Tests** - Verify that configuration loading works properly
3. **Project Structure Tests** - Verify that the project structure is as expected

## Adding New Tests

When adding new tests, follow these guidelines:

1. Create test files with the prefix `test_`
2. Group related tests in the same file
3. Use descriptive test names that clearly indicate what is being tested
4. Use fixtures from `conftest.py` when appropriate
