"""
Example client for the Ollama OpenAI-compatible API.
This demonstrates how to use the API from Python code.
"""

import requests
import json
import sys
import argparse
from dotenv import load_dotenv
import os

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Example client for the Ollama OpenAI-compatible API")
    parser.add_argument("--token", "-t", help="API token for authentication")
    parser.add_argument("--api-url", "-u", help="API base URL (default: http://localhost:8000)")
    parser.add_argument("--model", "-m", default="llama2", help="Model to use (default: llama2)")
    return parser.parse_args()

# Load arguments
args = parse_arguments()

# Load environment variables
load_dotenv()

# API configuration
API_BASE = args.api_url or "http://localhost:8000"
API_URL = f"{API_BASE}/v1/chat/completions"
API_TOKEN = args.token or os.environ.get("API_TOKENS", "test-token").split(",")[0]
DEFAULT_MODEL = args.model

def chat_with_llm(prompt, system_message=None, model=DEFAULT_MODEL):
    """
    Send a chat request to the API and return the response.
    
    Args:
        prompt (str): The user's message
        system_message (str, optional): System message to set context
        model (str, optional): The model to use, defaults to DEFAULT_MODEL
        
    Returns:
        str: The assistant's response
    """
    # Prepare the messages
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})
    
    # Prepare the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }
    
    # Send the request
    try:
        print(f"Sending request to {API_URL}...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            assistant_message = result["choices"][0]["message"]["content"]
            return assistant_message
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return f"Error: {response.status_code}"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: {str(e)}"

def interactive_chat():
    """Start an interactive chat session with the LLM."""
    print("\n" + "="*50)
    print("Interactive Chat with Local LLM")
    print("="*50)
    print("Type 'exit' or 'quit' to end the conversation.")
    print("Type 'system: <message>' to set a system message.")
    print("Type 'model: <model>' to change the model.")
    
    system_message = "You are a helpful assistant."
    model = DEFAULT_MODEL
    
    print(f"\nCurrent system message: \"{system_message}\"")
    print(f"Current model: {model}")
    print(f"Using API at: {API_URL}")
    print(f"Using token: {API_TOKEN[:4]}{'*' * (len(API_TOKEN) - 4)}")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
            
        if user_input.lower().startswith("system:"):
            system_message = user_input[7:].strip()
            print(f"System message updated to: \"{system_message}\"")
            continue
            
        if user_input.lower().startswith("model:"):
            model = user_input[6:].strip()
            print(f"Model updated to: {model}")
            continue
            
        if not user_input:
            continue
            
        print("\nAssistant: ", end="", flush=True)
        
        response = chat_with_llm(user_input, system_message, model)
        print(response)

if __name__ == "__main__":
    # Check if the API is running
    try:
        health_check = requests.get(f"{API_BASE}/health")
        if health_check.status_code == 200:
            print(f"API is running at {API_BASE}!")
        else:
            print(f"API is not responding correctly at {API_BASE}. Make sure it's running.")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"Cannot connect to the API at {API_BASE}. Make sure it's running.")
        print("Start the API with: python run_api.py --start")
        sys.exit(1)
    
    # Start interactive chat
    interactive_chat()
