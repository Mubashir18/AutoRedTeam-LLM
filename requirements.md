# AutoRedTeam-LLM Requirements & Prerequisites

This document outlines the system, software, and library requirements needed to build, configure, and execute the **AutoRedTeam-LLM** research engine locally.

---

## 💻 System & Hardware Requirements

Because the framework runs models entirely offline, performance depends on local system specs:

* **Operating System:** Windows 10/11, macOS (Apple Silicon supported), or Ubuntu 20.04/22.04 LTS.
* **Processor (CPU):** Multi-core processor (Intel Core i7/i9 10th Gen+, AMD Ryzen 7/9, or Apple M-series).
* **RAM:** 
  * *Minimum:* 16 GB (for running 7B quantized models like Mistral).
  * *Recommended:* 32 GB+.
* **GPU (Optional but Recommended):** 
  * NVIDIA GPU with 8 GB+ VRAM (NVIDIA CUDA support enabled) for fast token generation.
* **Storage:** 10 GB+ free disk space (for vector databases, text intelligence logs, and local model weights).

---

## 🛠️ Software Prerequisites

Ensure the following tools are installed before running the project:

1. **Python:** Version `3.10` or higher ([Download Python](https://www.python.org/downloads/)).
2. **Git:** For repository cloning ([Download Git](https://git-scm.com/)).
3. **Ollama:** Required to serve open-weight LLMs locally ([Download Ollama](https://ollama.ai/)).

---

## 📦 Python Dependencies

The project relies on the following key Python libraries:

```text
# Local LLM Serving
ollama>=0.1.20

# Vector Storage & RAG Processing
chromadb>=0.4.22
sentence-transformers>=2.2.2

# Data Scraping & HTTP Utilities
requests>=2.31.0
beautifulsoup4>=4.12.3

# Web GUI Dashboard
Flask>=3.0.2
Werkzeug>=3.0.1

# Utilities & Configuration Parsing
pyyaml>=6.0.1
pydantic>=2.6.0
