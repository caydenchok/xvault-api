# 🚀 XVault API - Ollama OpenAI-compatible API

A powerful, user-friendly FastAPI REST API that wraps local Ollama LLMs and provides a seamless OpenAI-compatible interface. Developed by Astra Gate Sdn. Bhd., based in Malaysia. ✨

## ✨ What Makes XVault API Special

XVault API stands out from other similar tools by focusing on:

- 🎯 **Simplicity First**: Clean, focused implementation that bridges Ollama and OpenAI's API format without unnecessary complexity
- 🙂 **User-Friendly Experience**: Streamlined setup process with intuitive command-line interface
- 🔒 **Secure Token Management**: Add and manage API tokens directly through command-line arguments
- 🧪 **Interactive Testing**: Built-in interactive client for immediate testing and experimentation
- 🛡️ **Comprehensive Error Handling**: Detailed logging and error reporting for easy troubleshooting
- 📚 **Educational Value**: Clean, well-commented code that serves as a learning resource

## 🔄 How It Works

XVault API acts as a bridge between your applications and local Ollama models:

```
┌───────────────┐     OpenAI-compatible     ┌───────────────┐     Ollama API     ┌───────────────┐
│               │        Requests           │               │      Requests      │               │
│  Applications ├────────────────────────────►   XVault API  ├────────────────────►    Ollama     │
│  (Frontend,   │                           │  (FastAPI)    │                    │  (Local LLM)  │
│   Scripts)    │◄───────────────────────────┤               │◄────────────────────┤               │
│               │     OpenAI-compatible     │               │     Responses      │               │
└───────────────┘        Responses          └───────────────┘                    └───────────────┘
```

This architecture allows you to:
1. Use existing OpenAI-compatible code with local models
2. Control access to your models with token authentication
3. Integrate with any application that supports the OpenAI API

For more details, see [architecture.md](architecture.md).

## 🌟 Features

- 🔌 OpenAI-compatible `/v1/chat/completions` endpoint
- 🔑 Flexible token-based authentication with command-line management
- 🌐 CORS enabled for seamless frontend integration
- 📊 Comprehensive request and response logging
- ⚠️ Robust error handling with proper HTTP status codes
- 💻 Interactive example client for testing and demonstration

## 📋 Prerequisites

- 🐍 Python 3.8+
- 🤖 [Ollama](https://github.com/ollama/ollama) installed and running locally
- 🧠 At least one model pulled in Ollama (e.g., `ollama pull llama2`)

### Setting Up Models

XVault API includes a helper script to manage Ollama models:

```bash
# List available models
python setup_models.py list

# See recommended models
python setup_models.py recommend

# Pull a specific model
python setup_models.py pull llama2
```

This makes it easy to get started with the right models for your needs.

## 🚀 Quick Start

### 🔥 The Easy Way (Recommended)

1. Make sure Ollama is installed and running with at least one model
2. Run the setup script:

   **Windows:**
   ```
   start_api.bat
   ```

   **Linux/Mac:**
   ```bash
   chmod +x start_api.sh
   ./start_api.sh
   ```

   Or simply:
   ```bash
   python run_api.py
   ```

This script will:
- Check if Ollama is running
- Set up a virtual environment
- Install dependencies
- Start the API server

### Command-line Options

You can customize the API using command-line options:

```bash
python run_api.py --token YOUR_API_TOKEN --port 8080 --start
```

Available options:
- `--token` or `-t`: Add a new API token for authentication
- `--ollama-api`: Set the Ollama API base URL (default: http://localhost:11434)
- `--port` or `-p`: Set the port to run the API on (default: 8000)
- `--host`: Set the host to bind the API to (default: 0.0.0.0)
- `--start` or `-s`: Start the API server immediately

Examples:
```bash
# Add a new API token and start the server
python run_api.py --token my-secure-token --start

# Change the port and start the server
python run_api.py --port 8080 --start

# Use a different Ollama instance
python run_api.py --ollama-api http://192.168.1.100:11434 --start
```

### Manual Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment variables by editing the `.env` file:
   ```
   API_TOKENS=your-secure-token-here
   OLLAMA_API_BASE=http://localhost:11434
   ```

4. Start the API server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

The API will be available at http://localhost:8000.

### Docker Deployment

XVault API includes Docker support for easy deployment:

#### Using Docker Compose (Recommended)

This method sets up both Ollama and XVault API in containers:

1. Make sure Docker and Docker Compose are installed
2. Run:
   ```bash
   docker-compose up -d
   ```
3. The API will be available at http://localhost:8000

To customize the configuration, edit the environment variables in the `docker-compose.yml` file.

#### Using Docker Alone

If you already have Ollama running elsewhere:

1. Build the Docker image:
   ```bash
   docker build -t xvault-api .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 \
     -e API_TOKENS=your-secure-token-here \
     -e OLLAMA_API_BASE=http://your-ollama-host:11434 \
     --name xvault-api \
     xvault-api
   ```

3. The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Usage

### Chat Completions

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -d '{
    "model": "llama2",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7
  }'
```

## Response Format

The API returns responses in the same format as the OpenAI API:

```json
{
  "id": "chatcmpl-123abc",
  "object": "chat.completion",
  "created": 1677858242,
  "model": "llama2",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I'm doing well, thank you for asking! How can I assist you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 16,
    "total_tokens": 41
  }
}
```

## Using the API

### Example Python Client

The repository includes an interactive example client that demonstrates how to use the API:

```bash
# Run the example client with default settings
python example_client.py

# Use a custom API token
python example_client.py --token your-api-token

# Connect to a different API endpoint
python example_client.py --api-url http://localhost:8080

# Use a specific model
python example_client.py --model mistral
```

The example client provides an interactive chat interface where you can:
- Chat with the LLM
- Change the system message with `system: Your system message here`
- Change the model with `model: modelname`
- Exit with `exit` or `quit`

### Code Examples in Different Languages

#### Python

```python
import requests

API_URL = "http://localhost:8000/v1/chat/completions"
API_TOKEN = "your-api-token"

def chat_with_llm(prompt, system_message=None):
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
        "model": "llama2",
        "messages": messages,
        "temperature": 0.7
    }

    # Send the request
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Example usage
system_msg = "You are a helpful assistant."
user_msg = "What is the capital of France?"
print(chat_with_llm(user_msg, system_msg))
```

#### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_URL = 'http://localhost:8000/v1/chat/completions';
const API_TOKEN = 'your-api-token';

async function chatWithLLM(prompt, systemMessage = null) {
  // Prepare the messages
  const messages = [];
  if (systemMessage) {
    messages.push({ role: 'system', content: systemMessage });
  }
  messages.push({ role: 'user', content: prompt });

  try {
    // Send the request
    const response = await axios.post(
      API_URL,
      {
        model: 'llama2',
        messages: messages,
        temperature: 0.7
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_TOKEN}`
        }
      }
    );

    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('Error:', error.response ? error.response.data : error.message);
    return `Error: ${error.message}`;
  }
}

// Example usage
const systemMsg = 'You are a helpful assistant.';
const userMsg = 'What is the capital of France?';
chatWithLLM(userMsg, systemMsg)
  .then(response => console.log(response))
  .catch(error => console.error(error));
```

#### React Frontend Integration

```javascript
import { useState } from 'react';

function ChatComponent() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'system', content: 'You are a helpful assistant.' }
  ]);
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const API_URL = 'http://localhost:8000/v1/chat/completions';
  const API_TOKEN = 'your-api-token';

  const callLLM = async (messages) => {
    try {
      setLoading(true);
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_TOKEN}`
        },
        body: JSON.stringify({
          model: 'llama2',
          messages: messages,
          temperature: 0.7
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.choices[0].message.content;
    } catch (error) {
      console.error('Error calling LLM:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message to chat
    const updatedMessages = [...messages, { role: 'user', content: input }];
    setMessages(updatedMessages);
    setInput('');

    try {
      // Get response from API
      const assistantResponse = await callLLM(updatedMessages);

      // Add assistant response to chat
      setMessages([...updatedMessages, { role: 'assistant', content: assistantResponse }]);
      setResponse(assistantResponse);
    } catch (error) {
      setResponse(`Error: ${error.message}`);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.filter(msg => msg.role !== 'system').map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <strong>{msg.role === 'user' ? 'You' : 'Assistant'}:</strong> {msg.content}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </form>
    </div>
  );
}
```

## Why Choose XVault API?

While there are several tools that provide OpenAI-compatible APIs for local LLMs, XVault API offers unique advantages:

1. **Focused Design**: Unlike general-purpose tools that try to do everything, XVault API does one thing exceptionally well - providing an OpenAI-compatible interface for Ollama.

2. **Minimal Learning Curve**: Get up and running in minutes with simple commands and clear documentation.

3. **Flexible Authentication**: The command-line token management makes it easy to secure your API without editing configuration files.

4. **Self-Contained Solution**: Everything you need is included in a single package with minimal dependencies.

5. **Production Ready**: Comprehensive error handling, logging, and CORS support make it suitable for both development and production environments.

## Troubleshooting

### Common Issues and Solutions

1. **API Connection Errors**
   - Ensure Ollama is running (`ollama serve` in a separate terminal)
   - Check if the port is already in use (try a different port with `--port`)
   - Verify your firewall isn't blocking the connection

2. **Authentication Errors**
   - Ensure you're using a valid token from your `.env` file
   - Check that your Authorization header is formatted correctly: `Bearer your-token`
   - Try adding a new token with `python run_api.py --token new-token`

3. **Model Not Found Errors**
   - Verify the model is pulled in Ollama (`ollama list`)
   - Pull the model if needed (`ollama pull modelname`)
   - Check for typos in the model name

4. **Performance Issues**
   - Larger models require more RAM and GPU resources
   - Consider using smaller models for faster responses
   - Adjust the `max_tokens` parameter to limit response length

### Getting Help

If you encounter issues not covered here, please:
1. Check the logs in the terminal where the API is running
2. Look for error messages in the API response
3. Contact us using the information below

## 🏢 About Astra Gate Sdn. Bhd.

XVault API is developed and maintained by **Astra Gate Sdn. Bhd.**, a technology company based in Kota Kinabalu, Sabah, Malaysia. We specialize in developing innovative solutions that bridge the gap between cutting-edge AI technologies and practical, user-friendly applications. 🌉

At Astra Gate, we believe in making advanced technology accessible to everyone. Our team combines deep technical expertise with a commitment to creating tools that are both powerful and easy to use. 💪

For more information about our company and other projects, please contact us at:

- 📧 **Email**: info@astragate.my
- 📍 **Location**: Kota Kinabalu, Sabah, Malaysia

## License

[MIT License](LICENSE)

---

*XVault API © 2023 Astra Gate Sdn. Bhd. All Rights Reserved.*
