# XVault API Architecture

```
┌───────────────┐     OpenAI-compatible     ┌───────────────┐     Ollama API     ┌───────────────┐
│               │        Requests           │               │      Requests      │               │
│  Applications ├────────────────────────────►   XVault API  ├────────────────────►    Ollama     │
│  (Frontend,   │                           │  (FastAPI)    │                    │  (Local LLM)  │
│   Scripts)    │◄───────────────────────────┤               │◄────────────────────┤               │
│               │     OpenAI-compatible     │               │     Responses      │               │
└───────────────┘        Responses          └───────────────┘                    └───────────────┘
```

## Flow Description

1. **Applications** send requests to XVault API using the OpenAI API format
   - These can be web frontends, scripts, or any client that works with OpenAI's API
   - Requests include model selection, messages, and parameters like temperature

2. **XVault API** processes these requests:
   - Authenticates using token-based authentication
   - Converts OpenAI format to Ollama format
   - Forwards the request to Ollama
   - Logs the request for debugging

3. **Ollama** processes the LLM request:
   - Runs inference on the local model
   - Returns the generated text

4. **XVault API** processes the response:
   - Converts Ollama's response format to OpenAI format
   - Adds token usage estimates
   - Returns the formatted response to the client

5. **Applications** receive responses in the familiar OpenAI format
   - This allows seamless integration with existing code

## Key Components

- **Token Authentication**: Secures the API with Bearer token authentication
- **Format Conversion**: Translates between OpenAI and Ollama formats
- **Error Handling**: Provides meaningful error messages
- **Logging**: Records requests and responses for debugging
- **CORS Support**: Enables browser-based applications to connect
