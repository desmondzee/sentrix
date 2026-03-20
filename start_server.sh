#!/bin/bash

# Start the inference server with configurable backend
# Usage: ./start_server.sh [llamacpp|sglang]

set -e

# Determine backend
BACKEND="${1:-llamacpp}"

if [ "$BACKEND" == "sglang" ]; then
    echo "Switching to SGLang server..."
    exec ./start_server_sglang.sh
fi

# Default: llama.cpp (best for macOS)
echo "=========================================="
echo "Starting llama.cpp Server"
echo "=========================================="

SERVER_BINARY="./llama.cpp/build/bin/llama-server"
MODEL_PATH="./models/qwen2.5-0.5b-instruct-q4_k_m.gguf"
HOST="127.0.0.1"
PORT="8080"

# Check if model exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "Error: Model not found at $MODEL_PATH"
    exit 1
fi

# Check if server binary exists
if [ ! -f "$SERVER_BINARY" ]; then
    echo "Error: Server binary not found at $SERVER_BINARY"
    echo "Building llama.cpp..."
    cd llama.cpp && cmake -B build -DLLAMA_BUILD_SERVER=ON && cmake --build build -j --target llama-server
    cd ..
fi

echo ""
echo "Configuration:"
echo "  Backend: llama.cpp (optimized for macOS)"
echo "  Model: $MODEL_PATH"
echo "  API Endpoint: http://$HOST:$PORT"
echo ""
echo "Features:"
echo "  - Metal GPU acceleration on Apple Silicon"
echo "  - GGUF format support"
echo "  - OpenAI-compatible API"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server with optimized settings for the model
$SERVER_BINARY \
    --model "$MODEL_PATH" \
    --host "$HOST" \
    --port "$PORT" \
    --ctx-size 4096 \
    --threads 4 \
    --n-predict -1 \
    --temp 0.7 \
    --top-p 0.9 \
    --repeat-penalty 1.1 \
    --chat-template qwen
