# AutoRedTeam-LLM: RAG-Driven Cybersecurity Intelligence Engine

AutoRedTeam-LLM is an open-source cybersecurity research framework combining Retrieval-Augmented Generation (RAG) with local open-weight Large Language Models (LLMs) to perform automated threat intelligence processing and defensive vulnerability analysis.

## ⚠️ Security & Ethics Disclaimer
This repository is published strictly for educational, academic, and defensive security research purposes. It is designed to assist security researchers and red teams in analyzing vulnerabilities and evaluating model alignment in isolated environments.

## 🏗 Architecture & Workflow
1. **Intelligence Collection**: Python scripts pull CVE and security intelligence into local text databases.
2. **Vector Indexing**: ChromaDB converts textual security records into vector embeddings.
3. **Local Inference**: Uses Ollama (`Mistral` base) for completely offline execution without external API dependencies.
4. **Interfaces**: Includes terminal-based CLI interface and web dashboard backend.

## 🚀 Installation & Quickstart

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.ai/) installed locally

### 2. Setup Environment
```bash
git clone [https://github.com/your-username/AutoRedTeam-LLM.git](https://github.com/your-username/AutoRedTeam-LLM.git)
cd AutoRedTeam-LLM
pip install -r requirements.txt
