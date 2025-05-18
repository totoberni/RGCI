import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.utils.env_utils import load_env_variables
from src.api.api_request_utils import get_response

def test_api():
    """Simple test function to verify OpenAI API connectivity"""
    # Load environment variables from the correct location
    loaded = load_env_variables()
    if not loaded:
        print("Failed to load environment variables from config/.env")
    
    # Get API key from environment variables
    api_key = os.environ.get('OPENAI_API_KEY')
    extractor_api_key = os.environ.get('OPENAI_API_KEY_EXTRACTOR', '')
    
    # Print debug information
    print(f"API_HOST: {os.environ.get('API_HOST', 'Not set')}")
    print(f"USER_AGENT: {os.environ.get('USER_AGENT', 'Not set')}")
    print(f"CONTENT_TYPE: {os.environ.get('CONTENT_TYPE', 'Not set')}")
    print(f"API_KEY present: {bool(api_key)}")
    print(f"EXTRACTOR_API_KEY present: {bool(extractor_api_key)}")
    
    # Print environment file path for debugging
    env_path = os.path.join(project_root, 'config', '.env')
    print(f"Environment file path: {env_path}")
    print(f"Environment file exists: {os.path.exists(env_path)}")
    
    if not api_key:
        print("\nERROR: No OpenAI API key found. Please check your config/.env file.")
        return
    
    # Test parameters
    model = "gpt-3.5-turbo"
    test_prompt = "Say 'Hello, API test successful!' if you can read this."
    
    print("\nSending test request to OpenAI API...")
    try:
        response = get_response(api_key, model, test_prompt)
        content = response["choices"][0]["message"]["content"]
        print("\nAPI Response:")
        print("-" * 50)
        print(content)
        print("-" * 50)
        print("\nAPI call successful!")
    except Exception as e:
        print(f"\nAPI call failed with error: {e}")
        print("\nDEBUG INFO:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Project root directory: {project_root}")
        print(f"Config directory: {os.path.join(project_root, 'config')}")
        print(f"Environment file path: {os.path.join(project_root, 'config', '.env')}")
        print(f"Environment file exists: {os.path.exists(os.path.join(project_root, 'config', '.env'))}")

if __name__ == "__main__":
    test_api() 