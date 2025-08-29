"""
Pytest configuration file for the silicon design environment tests.
"""

import os
import sys
import pytest
from pathlib import Path

# Add the project root to the Python path for importing modules
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

@pytest.fixture
def project_root():
    """Fixture to provide the project root path."""
    return PROJECT_ROOT

@pytest.fixture
def requirements_file():
    """Fixture to provide the requirements.txt file path."""
    return PROJECT_ROOT / "requirements.txt"

@pytest.fixture
def workspace_file():
    """Fixture to provide the WORKSPACE.bazel file path."""
    return PROJECT_ROOT / "WORKSPACE.bazel"
