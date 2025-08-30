# RISC-V Silicon Design Environment Documentation

This directory contains the Sphinx documentation for the RISC-V Silicon Design Environment.

## Building the Documentation

To build the documentation, you need to have Sphinx and other dependencies installed:

```bash
# Install documentation dependencies
pip install -r requirements.txt
```

Then, you can build the documentation:

```bash
# Build HTML documentation
make html
```

The built documentation will be available in the `_build/html` directory.

## Documentation Structure

The documentation is organized as follows:

- `getting_started/`: Getting started guides
- `user_guide/`: User guides
- `reference/`: Reference documentation
- `development/`: Development guides
- `_static/`: Static files (images, CSS, etc.)
- `_templates/`: Custom templates
- `_build/`: Built documentation (generated)

## Contributing to the Documentation

When contributing to the documentation, please follow these guidelines:

1. Use Markdown (`.md`) for new documents
2. Follow the existing structure
3. Include examples where appropriate
4. Use proper formatting
5. Update the index and toctrees as needed

## Building Other Formats

The documentation can be built in various formats:

```bash
# Build PDF documentation
make latexpdf

# Build EPUB documentation
make epub

# Build single HTML page
make singlehtml

# Build man pages
make man
```

## Generating API Documentation

The API documentation is generated automatically from docstrings using Sphinx's autodoc extension. To ensure your code is properly documented, follow these guidelines:

1. Use Google-style docstrings
2. Include type hints
3. Document all parameters, return values, and exceptions
4. Include examples where appropriate

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
        
    Raises:
        ValueError: If simulation results are invalid
        
    Example:
        >>> results = {"cycles": 100, "instructions": 80}
        >>> config = {"output_dir": "output/"}
        >>> metrics = calculate_performance_metrics(results, config)
        >>> print(metrics["ipc"])
        0.8
    """
    # Implementation
    return metrics
```
