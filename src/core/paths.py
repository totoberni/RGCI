"""
Path management module for the RGCI framework

This module centralizes all path-related configurations and operations to
ensure consistent path handling throughout the application.
"""
import os
from src.utils.env_utils import load_env_variables

# Load environment variables using our centralized utility function
load_env_variables()

# Define paths relative to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Get output path from environment or use default
ENV_OUTPUT_PATH = os.environ.get('OUTPUT_PATH', '')
if ENV_OUTPUT_PATH:
    # Check if it's an absolute path
    if os.path.isabs(ENV_OUTPUT_PATH):
        DATA_DIR = ENV_OUTPUT_PATH
    else:
        # Otherwise, consider it relative to project root
        DATA_DIR = os.path.join(PROJECT_ROOT, ENV_OUTPUT_PATH)
else:
    # Fallback to default
    DATA_DIR = os.path.join(PROJECT_ROOT, 'src', 'data')

# Derived paths
GENERATED_DATA_DIR = os.path.join(DATA_DIR, 'generated_data')
NAME_DATA_DIR = os.path.join(DATA_DIR, 'name_data')
PICKLE_DIR = os.path.join(GENERATED_DATA_DIR, 'pickle')
GRAPH_PNG_DIR = os.path.join(GENERATED_DATA_DIR, 'graph_png')
RESULT_DIR = os.path.join(GENERATED_DATA_DIR, 'result')

def ensure_directories():
    """Ensure all required directories exist, creating them if necessary."""
    for directory in [PICKLE_DIR, GRAPH_PNG_DIR, NAME_DATA_DIR, RESULT_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

# Export all path-related symbols
__all__ = [
    'PROJECT_ROOT',
    'DATA_DIR',
    'GENERATED_DATA_DIR',
    'NAME_DATA_DIR',
    'PICKLE_DIR',
    'GRAPH_PNG_DIR',
    'RESULT_DIR',
    'ensure_directories',
] 