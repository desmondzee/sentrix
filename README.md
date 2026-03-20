# Local LLM Server with llama.cpp

A simple on-device LLM server using llama.cpp with OpenAI-compatible API endpoints.

## Overview

This setup provides:
- **llama.cpp server** - Fast, efficient inference on CPU/GPU
- **Qwen2.5-0.5B-Instruct** - A small but capable SLM (~350MB)
- **OpenAI-compatible API** - `/v1/chat/completions` and `/completion` endpoints
- **Python client** - Easy-to-use client with interactive chat

## Quick Start

### 1. Start the Server

```bash
chmod +x start_server.sh
./start_server.sh
```

The server will start on `http://127.0.0.1:8080`

### 2. Use the Python Client

**Interactive chat:**
```bash
python3 client.py --chat
```

**Single prompt:**
```bash
python3 client.py --prompt "What is the capital of France?"
```

**With streaming:**
```bash
python3 client.py --prompt "Tell me a joke" --stream
```

### 3. Direct API Usage

**Chat Completion (OpenAI-compatible):**
```bash
curl -X POST http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7,
    "max_tokens": 512
  }'
```

**Simple Completion:**
```bash
curl -X POST http://127.0.0.1:8080/completion \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Once upon a time",
    "temperature": 0.7,
    "n_predict": 256
  }'
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /v1/chat/completions` | OpenAI-compatible chat completion |
| `POST /completion` | Simple text completion |
| `GET /health` | Server health check |
| `GET /models` | List available models |

## Client Options

```
python3 client.py [OPTIONS]

Options:
  -p, --prompt TEXT       Single prompt for completion
  -c, --chat              Interactive chat mode
  -t, --temperature FLOAT Sampling temperature (default: 0.7)
  -m, --max-tokens INT    Maximum tokens to generate (default: 512)
  -s, --stream            Stream the response
```

## Hardware Requirements

- **Memory**: ~500MB RAM
- **Storage**: ~400MB for the model
- **CPU**: Any modern CPU (Apple Silicon optimized)
- **GPU**: Optional (Metal support on Apple Silicon)

## Swapping Models

To use a different model:

1. Download a GGUF model from HuggingFace
2. Update the `MODEL_PATH` in `start_server.sh`
3. Restart the server

Popular small models:
- **Qwen2.5-0.5B** (~350MB) - Good general purpose
- **TinyLlama-1.1B** (~600MB) - Decent performance
- **Phi-2** (~1.6GB) - Strong reasoning

## Troubleshooting

**Server won't start:**
- Check if model file exists: `ls -lh models/`
- Check if port 8080 is in use: `lsof -i :8080`

**Connection errors:**
- Ensure server is running: `curl http://127.0.0.1:8080/health`
- Check firewall settings

**Slow responses:**
- Increase `--threads` in `start_server.sh` (match CPU cores)
- Use a smaller quantized model (Q4_K_M is a good balance)

## Project Structure

```
.
├── llama.cpp/              # llama.cpp source and build
├── models/                 # GGUF model files
│   └── qwen2.5-0.5b-instruct-q4_k_m.gguf
├── start_server.sh         # Server startup script
├── client.py               # Python API client
└── README.md               # This file
```

## License

- llama.cpp: MIT License
- Qwen2.5: Apache 2.0 License
