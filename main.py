import os
import json
import time
import uuid
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

import httpx
from fastapi import FastAPI, HTTPException, Depends, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from loguru import logger

# Configure logger
logger.add("api.log", rotation="10 MB", level="INFO")

# Initialize FastAPI app
app = FastAPI(
    title="Ollama OpenAI-compatible API",
    description="A FastAPI REST API that wraps the local Ollama LLM and mimics the OpenAI /v1/chat/completions endpoint",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Security
security = HTTPBearer()

# Load API tokens from environment or .env file
API_TOKENS = os.environ.get("API_TOKENS", "test-token").split(",")

# Ollama API endpoint
OLLAMA_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

# Models
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0
    user: Optional[str] = None

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: Usage

# Authentication dependency
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# Middleware for logging requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    logger.info(f"Request {request_id} started: {request.method} {request.url}")
    
    # Try to log the request body
    try:
        body = await request.body()
        if body:
            logger.info(f"Request {request_id} body: {body.decode()}")
        request = Request(request.scope, request._receive, request._send)
    except Exception as e:
        logger.error(f"Error reading request body: {e}")
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"Request {request_id} completed in {process_time:.4f}s with status {response.status_code}")
    
    return response

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"message": str(exc), "type": "internal_server_error"}},
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# Chat completions endpoint
@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(
    request: ChatCompletionRequest,
    token: str = Depends(verify_token),
):
    logger.info(f"Processing chat completion request for model: {request.model}")
    
    try:
        # Convert OpenAI-style request to Ollama format
        ollama_request = {
            "model": request.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "top_p": request.top_p,
            }
        }
        
        if request.max_tokens:
            ollama_request["options"]["num_predict"] = request.max_tokens
            
        if request.stop:
            ollama_request["options"]["stop"] = request.stop if isinstance(request.stop, list) else [request.stop]
        
        # Call Ollama API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_API_BASE}/api/chat",
                json=ollama_request,
                timeout=120.0,
            )
            
            if response.status_code != 200:
                logger.error(f"Ollama API error: {response.status_code} {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ollama API error: {response.text}",
                )
            
            ollama_response = response.json()
            
        # Convert Ollama response to OpenAI format
        completion_id = f"chatcmpl-{str(uuid.uuid4())}"
        created_time = int(time.time())
        
        # Extract the assistant's message
        assistant_message = ollama_response.get("message", {})
        
        # Estimate token counts (this is approximate)
        prompt_text = "".join([msg.content for msg in request.messages])
        completion_text = assistant_message.get("content", "")
        
        # Very rough token estimation (about 4 chars per token)
        prompt_tokens = len(prompt_text) // 4
        completion_tokens = len(completion_text) // 4
        total_tokens = prompt_tokens + completion_tokens
        
        return ChatCompletionResponse(
            id=completion_id,
            created=created_time,
            model=request.model,
            choices=[
                ChatCompletionResponseChoice(
                    index=0,
                    message=Message(
                        role=assistant_message.get("role", "assistant"),
                        content=assistant_message.get("content", ""),
                    ),
                    finish_reason="stop",
                )
            ],
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
            ),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error processing chat completion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat completion: {str(e)}",
        )

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
