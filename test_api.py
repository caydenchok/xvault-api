import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
API_URL = "http://localhost:8000/v1/chat/completions"
API_TOKEN = os.getenv("API_TOKENS", "test-token").split(",")[0]

def test_chat_completion():
    """Test the chat completion endpoint"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    payload = {
        "model": "llama2",  # Make sure this model is available in your Ollama
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a short poem about programming."}
        ],
        "temperature": 0.7
    }
    
    print(f"Sending request to {API_URL}...")
    response = requests.post(API_URL, headers=headers, json=payload)
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\nResponse:")
        print(json.dumps(result, indent=2))
        
        # Extract the assistant's message
        assistant_message = result["choices"][0]["message"]["content"]
        print("\nAssistant's response:")
        print(assistant_message)
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_chat_completion()
