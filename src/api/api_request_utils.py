import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables in case they haven't been loaded already
load_dotenv()

# Get environment variables with fallbacks
API_HOST = os.environ.get('API_HOST', 'api.openai.com')
USER_AGENT = os.environ.get('USER_AGENT', '')
CONTENT_TYPE = os.environ.get('CONTENT_TYPE', 'application/json')


def get_response(api_key, model, content):
    """
    Send a request to the OpenAI API and get the response using official SDK
    
    Args:
        api_key (str): The API key for authentication
        model (str): The model to use for generation
        content (str): The content to send to the model
        
    Returns:
        dict: The response from the API
    """
    # Create OpenAI client with the provided API key and custom configuration
    client = OpenAI(
        api_key=api_key,
        base_url=f"https://{API_HOST}/v1",
        default_headers={
            "Content-Type": CONTENT_TYPE,
            "User-Agent": USER_AGENT
        } if USER_AGENT else {"Content-Type": CONTENT_TYPE}
    )
    
    # Send request using the official SDK
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": content}
        ]
    )
    
    # Convert response to dictionary format for backward compatibility
    response_dict = {
        "choices": [
            {
                "message": {
                    "content": response.choices[0].message.content
                }
            }
        ]
    }
    
    return response_dict
