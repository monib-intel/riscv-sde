#!/usr/bin/env python3
"""
Configuration classes for the RISC-V SDE regression testing framework.
"""

import json
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TestConfig:
    """Configuration for a regression test."""
    project_name: str
    core_name: str
    expected_output: List[str]
    timeout: int = 30000  # Default timeout in milliseconds
    extra_args: Dict[str, Any] = None
    
    # Indicate to pytest that this is not a test class
    __test__ = False
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "project_name": self.project_name,
            "core_name": self.core_name,
            "expected_output": self.expected_output,
            "timeout": self.timeout,
            "extra_args": self.extra_args or {}
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary."""
        return cls(
            project_name=data["project_name"],
            core_name=data["core_name"],
            expected_output=data["expected_output"],
            timeout=data.get("timeout", 30000),
            extra_args=data.get("extra_args", {})
        )
    
    @classmethod
    def from_json_file(cls, json_path):
        """Create from JSON file."""
        with open(json_path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
