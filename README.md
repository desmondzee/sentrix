# Local LLM Server

A flexible inference server supporting both **llama.cpp** (macOS/local) and **SGLang** (Linux/GPU) backends.

## Quick Start

### Option 1: llama.cpp (Recommended for macOS)

Best for Apple Silicon with Metal GPU acceleration:

```bash
./start_server.sh
```

### Option 2: SGLang (Linux/GPU only)

For high-throughput GPU serving on Linux:

```bash
# Native (Linux with CUDA)
./start_server.sh sglang

# Or with Docker
HF_TOKEN=your_token docker-compose -f docker-compose.sglang.yml up
```

## Backend Comparison

| Feature | llama.cpp | SGLang |
|---------|-----------|--------|
| **Best For** | macOS/Apple Silicon | Linux + NVIDIA GPUs |
| **GPU Support** | Metal (macOS) | CUDA, ROCm |
| **Model Format** | GGUF | HuggingFace |
| **Throughput** | Good | Excellent |
| **Setup** | Simple | Complex (requires CUDA) |
| **macOS Support** | ✅ Native | ❌ Docker only |

## Usage

Once the server is running, use the same client:

```bash
# Interactive chat
python3 client.py --chat

# Single prompt
python3 client.py --prompt "What is the capital of France?"

# With streaming
python3 client.py --prompt "Tell me a story" --stream
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /v1/chat/completions` | OpenAI-compatible chat |
| `POST /completion` | Text completion |
| `GET /health` | Health check |
| `GET /models` | List available models |

## Configuration

Edit `config.yaml` to switch backends:

```yaml
backend: llamacpp  # or sglang

llamacpp:
  host: "127.0.0.1"
  port: 8080
  model: "./models/qwen2.5-0.5b-instruct-q4_k_m.gguf"
  
sglang:
  host: "127.0.0.1"
  port: 30000
  model: "Qwen/Qwen2.5-0.5B-Instruct"
  tp_size: 1
```

## Deploying SGLang on Linux

### Native Installation

```bash
# On Linux with CUDA
pip install sglang

# Start server
python3 -m sglang.launch_server \
    --model-path Qwen/Qwen2.5-0.5B-Instruct \
    --host 0.0.0.0 \
    --port 30000
```

### Docker Deployment

```bash
# Run SGLang in Docker (Linux only)
docker run --gpus all \
    --shm-size 32g \
    -p 30000:30000 \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HF_TOKEN=$HF_TOKEN" \
    --ipc=host \
    lmsysorg/sglang:latest \
    python3 -m sglang.launch_server \
      --model-path Qwen/Qwen2.5-0.5B-Instruct \
      --host 0.0.0.0 \
      --port 30000
```

### Kubernetes

See [SGLang K8s docs](https://docs.sglang.io/get_started/install.html#method-4-using-kubernetes)

## Switching Backends

```bash
# Use llama.cpp (default)
./start_server.sh

# Use SGLang
./start_server.sh sglang

# Or set via environment
BACKEND=sglang ./start_server.sh
```

## Project Structure

```
.
├── llama.cpp/              # llama.cpp source and build
├── sglang/                 # SGLang source (reference)
├── models/                 # GGUF models for llama.cpp
├── venv/                   # Python virtual environment
├── config.yaml             # Backend configuration
├── start_server.sh         # Main startup script
├── start_server_sglang.sh  # SGLang-specific startup
├── docker-compose.sglang.yml  # Docker setup for SGLang
├── client.py               # Python API client
└── README.md               # This file
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `BACKEND` | Choose backend: `llamacpp` or `sglang` |
| `SGLANG_HOST` | SGLang server host |
| `SGLANG_PORT` | SGLang server port |
| `SGLANG_MODEL` | HuggingFace model name |
| `SGLANG_TP_SIZE` | Tensor parallelism (GPUs) |
| `HF_TOKEN` | HuggingFace token for gated models |

## Hardware Requirements

### llama.cpp (macOS)
- **Memory**: ~500MB RAM
- **GPU**: Apple Silicon (Metal) or CPU
- **Storage**: ~400MB per model

### SGLang (Linux)
- **GPU**: NVIDIA GPU with 8GB+ VRAM
- **Memory**: 16GB+ RAM
- **Storage**: ~2GB per model
- **OS**: Linux (Ubuntu 20.04+ recommended)

## Troubleshooting

### llama.cpp on macOS
```bash
# If server won't start
lsof -i :8080  # Check port usage
pkill -f llama-server  # Kill existing server
```

### SGLang on Linux
```bash
# Check CUDA is available
nvidia-smi

# If OOM errors, reduce memory fraction
python3 -m sglang.launch_server --mem-fraction 0.70 ...
```

## License

- llama.cpp: MIT License
- SGLang: Apache 2.0 License
- Models: See respective HuggingFace pages
