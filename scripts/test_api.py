import sys
import os
import argparse
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.utils.env_utils import load_env_variables
from src.api.api_request_utils import get_response
from src.core.settings import DEFAULT_EXTRACTOR_MODEL, SECONDARY_EXTRACTOR_MODEL

def test_api(model_to_test=None):
    """Simple test function to verify OpenAI API connectivity
    
    Args:
        model_to_test: Optional model name to test. If None, tests with both default models.
    """
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
    
    # Test parameters for base model
    base_model = "gpt-3.5-turbo"
    test_prompt = "Say 'Hello, API test successful!' if you can read this."
    
    print("\nSending test request to OpenAI API with base model...")
    try:
        response = get_response(api_key, base_model, test_prompt)
        content = response["choices"][0]["message"]["content"]
        print("\nAPI Response (Base Model):")
        print("-" * 50)
        print(content)
        print("-" * 50)
        print("\nBase model API call successful!")
    except Exception as e:
        print(f"\nBase model API call failed with error: {e}")
        print("\nDEBUG INFO:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Project root directory: {project_root}")
        print(f"Config directory: {os.path.join(project_root, 'config')}")
        print(f"Environment file path: {os.path.join(project_root, 'config', '.env')}")
        print(f"Environment file exists: {os.path.exists(os.path.join(project_root, 'config', '.env'))}")
    
    # Test extractor models if requested or if no specific model was requested
    if not model_to_test or model_to_test in [DEFAULT_EXTRACTOR_MODEL, SECONDARY_EXTRACTOR_MODEL]:
        # Determine which models to test
        models_to_test = []
        if not model_to_test:
            models_to_test = [DEFAULT_EXTRACTOR_MODEL, SECONDARY_EXTRACTOR_MODEL]
        else:
            models_to_test = [model_to_test]
            
        for extractor_model in models_to_test:
            test_extractor_model(extractor_api_key or api_key, extractor_model, test_prompt)

def test_extractor_model(api_key, model_name, test_prompt):
    """Test a specific extractor model
    
    Args:
        api_key: API key to use
        model_name: Model name to test
        test_prompt: Test prompt to send
    """
    print(f"\nSending test request to OpenAI API with extractor model: {model_name}...")
    try:
        response = get_response(api_key, model_name, test_prompt)
        content = response["choices"][0]["message"]["content"]
        print(f"\nAPI Response ({model_name}):")
        print("-" * 50)
        print(content)
        print("-" * 50)
        print(f"\n{model_name} API call successful!")
    except Exception as e:
        print(f"\n{model_name} API call failed with error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test OpenAI API connectivity')
    parser.add_argument('--model', help='Model to test (default, secondary, or specific model name)')
    args = parser.parse_args()
    
    model_to_test = None
    if args.model:
        if args.model.lower() == 'default':
            model_to_test = DEFAULT_EXTRACTOR_MODEL
        elif args.model.lower() == 'secondary':
            model_to_test = SECONDARY_EXTRACTOR_MODEL
        else:
            model_to_test = args.model
            
    test_api(model_to_test) 