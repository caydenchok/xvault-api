# Contributing to XVault API

Thank you for considering contributing to XVault API! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any relevant logs or screenshots
- Your environment (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please create an issue with:

- A clear, descriptive title
- A detailed description of the proposed feature
- Any relevant examples or use cases
- If possible, an implementation approach

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Open a Pull Request

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/caydenchok/xvault-api.git
   cd xvault-api
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Make sure Ollama is installed and running:
   ```bash
   ollama serve
   ```

4. Run the API:
   ```bash
   python run_api.py --start
   ```

## Coding Guidelines

- Follow PEP 8 style guidelines for Python code
- Write clear, descriptive commit messages
- Include docstrings for all functions, classes, and modules
- Add tests for new features
- Update documentation when necessary

## Testing

Run tests to ensure your changes don't break existing functionality:

```bash
pytest
```

## Documentation

If you're adding or changing features, please update the relevant documentation:

- README.md for general usage and installation
- Code comments and docstrings
- architecture.md for architectural changes

## Questions?

If you have any questions about contributing, please open an issue with your question.

Thank you for contributing to XVault API!
