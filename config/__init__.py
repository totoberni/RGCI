"""
Configuration settings for the RGCI framework
"""
import os
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Import settings from core modules
from src.core.settings import (
    get_test_settings,
    get_data_gen_settings,
)

# Import paths from the paths module
from src.core.paths import (
    PROJECT_ROOT,
    DATA_DIR,
    GENERATED_DATA_DIR,
    NAME_DATA_DIR,
    PICKLE_DIR,
    GRAPH_PNG_DIR,
    RESULT_DIR,
    ensure_directories
)

__all__ = [
    'get_test_settings',
    'get_data_gen_settings',
    'PROJECT_ROOT',
    'DATA_DIR',
    'GENERATED_DATA_DIR',
    'NAME_DATA_DIR',
    'PICKLE_DIR',
    'GRAPH_PNG_DIR',
    'RESULT_DIR',
    'ensure_directories'
] 