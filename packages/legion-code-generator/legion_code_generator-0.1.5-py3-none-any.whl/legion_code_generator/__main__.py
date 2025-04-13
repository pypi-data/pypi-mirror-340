"""Main entry point for the module when run with python -m legion_code_generator"""
import os
import sys

# Add the parent directory to ensure imports work correctly
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, current_dir)

try:
    from legion_code_generator.agent import main
except ImportError:
    # If that fails, try relative import
    from .agent import main

if __name__ == "__main__":
    main() 