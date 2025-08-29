"""
Pytest configuration file for the silicon design environment tests.
"""

import os
import sys
import pytest
from pathlib import Path

# Add the project root to the Python path for importing modules
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

# Add the validate directory to the path
VALIDATE_ROOT = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(VALIDATE_ROOT))

# Import the regression runner
from tools.regression import RegressionRunner

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

@pytest.fixture
def regression_runner():
    """Fixture to provide a regression runner."""
    return RegressionRunner(PROJECT_ROOT)
