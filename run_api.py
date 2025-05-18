"""
Simple script to run the Ollama OpenAI-compatible API.
This handles checking dependencies and starting the server.
"""

import os
import sys
import subprocess
import time
import requests
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)
    print("✅ Python version is compatible.")

def check_ollama_running():
    """Check if Ollama is running."""
    print("Checking if Ollama is running...")
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print(f"✅ Ollama is running with the following models:")
                for model in models:
                    print(f"   - {model['name']}")
            else:
                print("⚠️ Ollama is running but no models are available.")
                print("   Please pull a model with: ollama pull llama2")
            return True
        else:
            print("❌ Ollama API responded with an error.")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama is not running. Please start Ollama first.")
        print("   You can download Ollama from: https://ollama.ai/")
        return False

def setup_virtual_env():
    """Set up a virtual environment if it doesn't exist."""
    venv_dir = Path("venv")

    if not venv_dir.exists():
        print("Setting up virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created.")
    else:
        print("✅ Virtual environment already exists.")

    # Determine the pip path based on the platform
    if sys.platform == "win32":
        pip_path = venv_dir / "Scripts" / "pip"
    else:
        pip_path = venv_dir / "bin" / "pip"

    # Install requirements
    print("Installing dependencies...")
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
    print("✅ Dependencies installed.")

def start_api_server(host="0.0.0.0", port=8000):
    """Start the FastAPI server."""
    print("\n" + "="*50)
    print(f"Starting the Ollama OpenAI-compatible API server on {host}:{port}...")
    print("="*50)

    # Determine the uvicorn path based on the platform
    if sys.platform == "win32":
        uvicorn_path = Path("venv") / "Scripts" / "uvicorn"
    else:
        uvicorn_path = Path("venv") / "bin" / "uvicorn"

    # Start the server
    try:
        subprocess.run([
            str(uvicorn_path),
            "main:app",
            "--host", host,
            "--port", str(port),
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped.")

def update_env_file(api_token=None, ollama_api_base=None):
    """Update the .env file with new values."""
    # Load current values
    load_dotenv()
    current_tokens = os.environ.get("API_TOKENS", "test-token")
    current_ollama_api = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

    # Update with new values if provided
    if api_token:
        # Check if token already exists
        tokens = current_tokens.split(",")
        if api_token not in tokens:
            tokens.append(api_token)
            current_tokens = ",".join(tokens)

    if ollama_api_base:
        current_ollama_api = ollama_api_base

    # Write to .env file
    with open(".env", "w") as f:
        f.write(f"# API configuration\n")
        f.write(f"API_TOKENS={current_tokens}\n")
        f.write(f"OLLAMA_API_BASE={current_ollama_api}\n")

    print(f"✅ Updated .env file with API tokens: {current_tokens}")
    return current_tokens.split(",")[0]  # Return the first token for examples

def main():
    """Main function to run the API."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the Ollama OpenAI-compatible API")
    parser.add_argument("--token", "-t", help="API token to add for authentication")
    parser.add_argument("--ollama-api", help="Ollama API base URL (default: http://localhost:11434)")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port to run the API on (default: 8000)")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the API to (default: 0.0.0.0)")
    parser.add_argument("--start", "-s", action="store_true", help="Start the API server immediately")
    args = parser.parse_args()

    print("\n" + "="*50)
    print("Ollama OpenAI-compatible API Setup")
    print("="*50 + "\n")

    check_python_version()

    if not check_ollama_running():
        sys.exit(1)

    # Update .env file if token or API base is provided
    example_token = update_env_file(args.token, args.ollama_api)

    setup_virtual_env()

    print("\n" + "="*50)
    print("Setup complete! You can now use the API.")
    print("="*50)
    print(f"\nAPI will be available at: http://localhost:{args.port}")
    print(f"API documentation: http://localhost:{args.port}/docs")
    print("\nExample usage:")
    print(f"""
curl -X POST http://localhost:{args.port}/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer {example_token}" \\
  -d '{{
    "model": "llama2",
    "messages": [
      {{"role": "system", "content": "You are a helpful assistant."}},
      {{"role": "user", "content": "Hello, how are you?"}}
    ],
    "temperature": 0.7
  }}'
    """)

    # Start the server if --start flag is provided or ask the user
    if args.start:
        start_api_server(args.host, args.port)
    else:
        # Ask user if they want to start the server
        while True:
            choice = input("\nDo you want to start the API server now? (y/n): ").lower()
            if choice in ['y', 'yes']:
                start_api_server(args.host, args.port)
                break
            elif choice in ['n', 'no']:
                print(f"\nYou can start the server later with: python run_api.py --start --port {args.port}")
                break
            else:
                print("Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
