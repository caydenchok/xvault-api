"""
Helper script to pull and manage Ollama models for use with XVault API.
"""

import subprocess
import sys
import json
import requests
import argparse
from typing import List, Dict, Any

def check_ollama_running() -> bool:
    """Check if Ollama is running."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def get_available_models() -> List[Dict[str, Any]]:
    """Get list of available models from Ollama."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            return response.json().get("models", [])
        return []
    except requests.exceptions.ConnectionError:
        return []

def pull_model(model_name: str) -> bool:
    """Pull a model from Ollama."""
    print(f"Pulling model: {model_name}...")
    try:
        result = subprocess.run(
            ["ollama", "pull", model_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error pulling model: {e}")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("Error: Ollama command not found. Make sure Ollama is installed.")
        return False

def list_models() -> None:
    """List all available models."""
    models = get_available_models()
    
    if not models:
        print("No models found. Pull some models first.")
        return
    
    print("\nAvailable models:")
    print("-" * 60)
    print(f"{'Model Name':<20} {'Size':<10} {'Modified Date':<20}")
    print("-" * 60)
    
    for model in models:
        name = model.get("name", "Unknown")
        size = model.get("size", 0) // (1024 * 1024)  # Convert to MB
        modified = model.get("modified", "Unknown")
        print(f"{name:<20} {size:>8} MB {modified:<20}")

def recommend_models() -> None:
    """Recommend some popular models to try."""
    recommendations = [
        {"name": "llama2", "description": "Meta's Llama 2 model (7B)"},
        {"name": "mistral", "description": "Mistral 7B model"},
        {"name": "phi", "description": "Microsoft's Phi-2 model (2.7B)"},
        {"name": "gemma", "description": "Google's Gemma model (2B)"},
        {"name": "orca-mini", "description": "Orca Mini model (3B)"},
        {"name": "neural-chat", "description": "Intel's Neural Chat model (7B)"},
    ]
    
    print("\nRecommended models to try:")
    print("-" * 60)
    print(f"{'Model Name':<15} {'Description':<40}")
    print("-" * 60)
    
    for model in recommendations:
        print(f"{model['name']:<15} {model['description']:<40}")

def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description="Manage Ollama models for XVault API")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available models")
    
    # Pull command
    pull_parser = subparsers.add_parser("pull", help="Pull a model from Ollama")
    pull_parser.add_argument("model", help="Model name to pull")
    
    # Recommend command
    recommend_parser = subparsers.add_parser("recommend", help="Show recommended models")
    
    args = parser.parse_args()
    
    if not check_ollama_running():
        print("Error: Ollama is not running. Please start Ollama first.")
        sys.exit(1)
    
    if args.command == "list":
        list_models()
    elif args.command == "pull":
        pull_model(args.model)
    elif args.command == "recommend":
        recommend_models()
    else:
        # Default behavior if no command is provided
        list_models()
        print("\n")
        recommend_models()
        
        print("\nTo pull a model, use:")
        print("  python setup_models.py pull MODEL_NAME")

if __name__ == "__main__":
    main()
