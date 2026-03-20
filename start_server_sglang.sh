#!/bin/bash

# Start SGLang server for Linux/GPU deployment
# Note: SGLang requires CUDA and Linux. Use Docker on macOS for testing only.

set -e

echo "=========================================="
echo "Starting SGLang Server"
echo "=========================================="

# Configuration
HOST="${SGLANG_HOST:-127.0.0.1}"
PORT="${SGLANG_PORT:-30000}"
MODEL="${SGLANG_MODEL:-Qwen/Qwen2.5-0.5B-Instruct}"
TP_SIZE="${SGLANG_TP_SIZE:-1}"  # Tensor parallelism (number of GPUs)

# Check if we're on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "WARNING: SGLang is designed for Linux with CUDA."
    echo "Current OS: $OSTYPE"
    echo ""
    echo "Options:"
    echo "1. Use llama.cpp instead: ./start_server.sh"
    echo "2. Run SGLang in Docker (CPU-only, very slow):"
    echo "   docker run --rm -p $PORT:$PORT lmsysorg/sglang:latest \\"
    echo "     python3 -m sglang.launch_server \\"
    echo "     --model-path $MODEL --host $HOST --port $PORT"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if Python and sglang are available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

# Check if sglang is installed
if ! python3 -c "import sglang" 2>/dev/null; then
    echo "Installing SGLang..."
    pip install sglang
fi

# For HuggingFace models, ensure the model is accessible
# You may need to set HF_TOKEN for gated models
if [ -n "$HF_TOKEN" ]; then
    echo "Using HuggingFace token from environment"
    export HF_TOKEN
fi

echo ""
echo "Configuration:"
echo "  Model: $MODEL"
echo "  Host: $HOST"
echo "  Port: $PORT"
echo "  Tensor Parallelism: $TP_SIZE"
echo ""
echo "Starting server..."
echo "API will be available at: http://$HOST:$PORT"
echo "Press Ctrl+C to stop"
echo ""

# Start SGLang server
python3 -m sglang.launch_server \
    --model-path "$MODEL" \
    --host "$HOST" \
    --port "$PORT" \
    --tp-size "$TP_SIZE" \
    --mem-fraction 0.85 \
    --enable-metrics \
    "$@"
