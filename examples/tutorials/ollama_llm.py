#!/usr/bin/env python
"""
Ollama LLM server example using python-a2a

This script runs two A2A servers:
1. A basic Ollama LLM server on port 5001
2. A travel guide chain server on port 5002

Prerequisites:
  - Install langchain-openai: uv pip install langchain-openai
  - Install langchain-ollama: uv pip install langchain-ollama
  - Have Ollama running locally with the llama3.2 model available

Usage:
  uv run ./examples/ollama/ollama_llm.py

Press Ctrl+C to stop the servers.
"""

#from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from python_a2a import A2AClient, run_server
from python_a2a.langchain import to_a2a_server
from langchain_ollama.llms import OllamaLLM
import os


os.environ["GRPC_VERBOSITY"] = "ERROR"

# Create a LangChain LLM
#llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm = OllamaLLM(model="llama3.2:latest")

# Convert LLM to A2A server
llm_server = to_a2a_server(llm)

# Create a simple chain
template = "You are a helpful travel guide.\n\nQuestion: {query}\n\nAnswer:"
prompt = PromptTemplate.from_template(template)
travel_chain = prompt | llm | StrOutputParser()

# Convert chain to A2A server
travel_server = to_a2a_server(travel_chain)

# Run servers in background threads

import threading
import signal
import sys

def main():
    llm_thread = threading.Thread(
        target=lambda: run_server(llm_server, port=5001),
        daemon=True
    )
    llm_thread.start()

    travel_thread = threading.Thread(
        target=lambda: run_server(travel_server, port=5002),
        daemon=True
    )
    travel_thread.start()

    # Wait here until Ctrl+C
    try:
        print("Servers are running. Press Ctrl+C to stop.")
        signal.pause()  # Wait for signals
    except KeyboardInterrupt:
        print("\nStopping servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()
