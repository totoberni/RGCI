import os
from openai import OpenAI


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
    # Create OpenAI client with the provided API key
    client = OpenAI(api_key=api_key)
    
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
