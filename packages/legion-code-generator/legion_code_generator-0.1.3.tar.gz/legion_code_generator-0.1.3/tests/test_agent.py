"""Basic tests for the agent module."""

import pytest
import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from the package
from legion_code_generator.agent import CodingAgent

def test_agent_init():
    """Test agent initialization without a project path."""
    agent = CodingAgent()
    assert agent is not None
    assert agent.context is not None
    assert agent.executor is not None

def test_agent_with_project_path():
    """Test agent initialization with a project path."""
    test_path = Path("./test_project")
    # Create the test directory if it doesn't exist
    test_path.mkdir(exist_ok=True)
    
    try:
        agent = CodingAgent(test_path)
        assert agent is not None
        assert agent.context is not None
        assert agent.context.project_path == test_path
    finally:
        # Clean up - remove the test directory if it's empty
        if test_path.exists() and not any(test_path.iterdir()):
            test_path.rmdir() 