#!/usr/bin/env python3
"""
Simple API client for llama.cpp server
Supports chat completion and simple prompt inference
"""

import requests
import json
import argparse
from typing import Optional

BASE_URL = "http://127.0.0.1:8080"


def chat_completion(
    messages: list,
    temperature: float = 0.7,
    max_tokens: int = 512,
    stream: bool = False
) -> str:
    """
    Send a chat completion request to the server.
    
    Args:
        messages: List of dicts with 'role' and 'content' keys
        temperature: Sampling temperature (0.0 - 1.0)
        max_tokens: Maximum tokens to generate
        stream: Whether to stream the response
    
    Returns:
        The generated response text
    """
    url = f"{BASE_URL}/v1/chat/completions"
    
    payload = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
    }
    
    response = requests.post(url, json=payload, stream=stream)
    response.raise_for_status()
    
    if stream:
        # Handle streaming response
        result = ""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk.get('choices', [{}])[0].get('delta', {})
                        content = delta.get('content', '')
                        if content:
                            result += content
                            print(content, end='', flush=True)
                    except json.JSONDecodeError:
                        pass
        print()  # Newline after streaming
        return result
    else:
        # Handle non-streaming response
        data = response.json()
        return data['choices'][0]['message']['content']


def simple_prompt(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 512,
    stream: bool = False
) -> str:
    """
    Send a simple prompt completion request to the server.
    
    Args:
        prompt: The text prompt
        temperature: Sampling temperature (0.0 - 1.0)
        max_tokens: Maximum tokens to generate
        stream: Whether to stream the response
    
    Returns:
        The generated response text
    """
    url = f"{BASE_URL}/completion"
    
    payload = {
        "prompt": prompt,
        "temperature": temperature,
        "n_predict": max_tokens,
        "stream": stream
    }
    
    response = requests.post(url, json=payload, stream=stream)
    response.raise_for_status()
    
    if stream:
        # Handle streaming response
        result = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    content = data.get('content', '')
                    if content:
                        result += content
                        print(content, end='', flush=True)
                except json.JSONDecodeError:
                    pass
        print()  # Newline after streaming
        return result
    else:
        # Handle non-streaming response
        data = response.json()
        return data['content']


def interactive_chat():
    """Run an interactive chat session with the model."""
    print("=" * 50)
    print("Interactive Chat with Local LLM")
    print("Type 'exit' or 'quit' to end the conversation")
    print("=" * 50)
    print()
    
    messages = []
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            print("Assistant: ", end='', flush=True)
            response = chat_completion(messages, stream=True)
            messages.append({"role": "assistant", "content": response})
            print()
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to server. Is it running?")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Client for llama.cpp server API'
    )
    parser.add_argument(
        '--prompt', '-p',
        help='Single prompt for completion (non-interactive)'
    )
    parser.add_argument(
        '--chat', '-c',
        action='store_true',
        help='Interactive chat mode'
    )
    parser.add_argument(
        '--temperature', '-t',
        type=float,
        default=0.7,
        help='Sampling temperature (default: 0.7)'
    )
    parser.add_argument(
        '--max-tokens', '-m',
        type=int,
        default=512,
        help='Maximum tokens to generate (default: 512)'
    )
    parser.add_argument(
        '--stream', '-s',
        action='store_true',
        help='Stream the response'
    )
    
    args = parser.parse_args()
    
    try:
        if args.chat:
            interactive_chat()
        elif args.prompt:
            result = simple_prompt(
                args.prompt,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                stream=args.stream
            )
            if not args.stream:
                print(result)
        else:
            # Default: interactive chat
            interactive_chat()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to server at {BASE_URL}")
        print("Make sure the server is running: ./start_server.sh")


if __name__ == "__main__":
    main()
