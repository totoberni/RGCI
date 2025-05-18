"""
Configuration settings for the RGCI framework
"""
import os
from dotenv import load_dotenv
from config.settings import (
    get_test_settings,
    get_data_gen_settings,
    PROJECT_ROOT,
    DATA_DIR,
    GENERATED_DATA_DIR,
    NAME_DATA_DIR,
    PICKLE_DIR,
    GRAPH_PNG_DIR
)

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

__all__ = [
    'get_test_settings',
    'get_data_gen_settings',
    'PROJECT_ROOT',
    'DATA_DIR',
    'GENERATED_DATA_DIR',
    'NAME_DATA_DIR',
    'PICKLE_DIR',
    'GRAPH_PNG_DIR'
] 