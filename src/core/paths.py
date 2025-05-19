"""
Path management module for the RGCI framework

This module centralizes all path-related configurations and operations to
ensure consistent path handling throughout the application.
"""
import os
import time
from src.utils.env_utils import load_env_variables

# Load environment variables using our centralized utility function
load_env_variables()

# Define utility functions first
def normalize_path(path):
    """Normalize a file path to use the correct path separators for the current OS."""
    return os.path.normpath(path) if path else path

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

# Check if DATA_DIR already ends with 'generated_data'
if os.path.basename(normalize_path(DATA_DIR)) == 'generated_data':
    # Already points to a generated_data directory, use it directly
    GENERATED_DATA_DIR = DATA_DIR
else:
    # Add 'generated_data' to the path
    GENERATED_DATA_DIR = os.path.join(DATA_DIR, 'generated_data')

NAME_DATA_DIR = os.path.join(DATA_DIR, 'name_data')
PICKLE_DIR = os.path.join(GENERATED_DATA_DIR, 'pickle')
GRAPH_PNG_DIR = os.path.join(GENERATED_DATA_DIR, 'graph_png')
RESULT_DIR = os.path.join(GENERATED_DATA_DIR, 'result')

# Model-specific result directories will be constructed with get_model_result_dirs()

def file_exists(file_path):
    """Check if a file exists, after normalizing the path."""
    path = normalize_path(file_path)
    return os.path.isfile(path)

def dir_exists(dir_path):
    """Check if a directory exists, after normalizing the path."""
    path = normalize_path(dir_path)
    return os.path.isdir(path)

def safe_join_path(*paths):
    """Join paths and normalize the result."""
    return normalize_path(os.path.join(*paths))

def get_model_result_dirs(model_name):
    """
    Get the directory paths for test, answer extraction, and evaluation results
    for a specific model.
    
    Returns:
        tuple: (model_dir, test_dir, ans_ex_dir, eval_dir)
    """
    model_dir = safe_join_path(RESULT_DIR, model_name)
    test_dir = safe_join_path(model_dir, 'test')
    ans_ex_dir = safe_join_path(model_dir, 'ans_ex')
    eval_dir = safe_join_path(model_dir, 'eval')
    return model_dir, test_dir, ans_ex_dir, eval_dir

def get_file_path(base_dir, task, graph_shape_group, name_type, prompt_type, file_ext="json"):
    """
    Construct a file path for a test, answer extraction, or evaluation file.
    
    Args:
        base_dir: Base directory path (test, ans_ex, or eval)
        task: Task type (conf_ce_path, etc.)
        graph_shape_group: Graph shape group (00, 01, etc.)
        name_type: Name type (specific, bio, etc.)
        prompt_type: Prompt type (zero_shot, one_shot, etc.)
        file_ext: File extension (default 'json')
    
    Returns:
        str: Normalized file path
    """
    indicators = [task, graph_shape_group, name_type, prompt_type]
    file_name = "_".join(indicators)
    return safe_join_path(base_dir, f"{file_name}.{file_ext}")

def wait_for_file(file_path, max_retries=10, delay=5):
    """
    Wait for a file to become available, with retries.
    
    Args:
        file_path: Path to the file to wait for
        max_retries: Maximum number of retries (default 10)
        delay: Delay between retries in seconds (default 5)
    
    Returns:
        bool: True if file exists, False if max retries reached
    """
    path = normalize_path(file_path)
    retries = 0
    
    while retries < max_retries:
        if file_exists(path):
            return True
        
        print(f"File not found, retrying ({retries+1}/{max_retries}): {path}", flush=True)
        time.sleep(delay)
        retries += 1
    
    return False

def ensure_directories():
    """Ensure all required directories exist, creating them if necessary."""
    base_dirs = [PICKLE_DIR, GRAPH_PNG_DIR, NAME_DATA_DIR, RESULT_DIR]
    
    # Create base directories
    for directory in base_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # We don't automatically create model-specific directories
    # These will be created as needed by the run_evaluation.py

# Export all path-related symbols
__all__ = [
    'PROJECT_ROOT',
    'DATA_DIR',
    'GENERATED_DATA_DIR',
    'NAME_DATA_DIR',
    'PICKLE_DIR',
    'GRAPH_PNG_DIR',
    'RESULT_DIR',
    'normalize_path',
    'file_exists',
    'dir_exists',
    'safe_join_path',
    'get_model_result_dirs',
    'get_file_path',
    'wait_for_file',
    'ensure_directories',
] 