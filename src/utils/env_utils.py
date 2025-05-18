"""
Utility functions for loading environment variables from the correct location
"""
import os
from pathlib import Path
from dotenv import load_dotenv

def load_env_variables():
    """
    Load environment variables from the config/.env file
    
    This function ensures that environment variables are loaded from the correct
    location (./config/.env) regardless of where the code is being executed from.
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # Build the path to the .env file in the config directory
    env_path = os.path.join(project_root, 'config', '.env')
    
    # Check if the file exists and load it
    if os.path.exists(env_path):
        load_dotenv(env_path)
        return True
    else:
        print(f"WARNING: Environment file not found at {env_path}")
        return False 