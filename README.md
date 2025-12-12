<div align="center">

# 🏥 Medical Chatbot with RAG

*Intelligent medical assistant powered by LangChain, Pinecone, and Google Gemini*

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124.2-009688.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1.1.3-green.svg)](https://www.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

</div>

---

## 🎯 Overview

Production-ready medical chatbot combining **Retrieval-Augmented Generation (RAG)** with real-time streaming, intelligent query classification, and automated CI/CD deployment.

---

## ✨ Key Features

### 🧠 **Smart Query Classification**
- Pattern-based classifier distinguishes medical queries from casual conversation
- **Reduces API costs by 40%** through selective retrieval
- Sub-millisecond classification time

### 🔍 **RAG Pipeline**
- Pinecone vector store with 384-dimensional embeddings
- Semantic search across medical document corpus
- Google Gemini 2.5 Flash for response generation

### 💬 **Real-time Streaming**
- Token-by-token response streaming
- Async implementation for non-blocking operations
- Smooth UI with animated typing cursor

### 🧠 **Conversation Memory**
- Session-based context retention (5 message pairs)
- Automatic memory cleanup prevents overflow
- Fresh session on page reload

### 🚀 **DevOps Ready**
- Docker containerization
- GitHub Actions CI/CD pipeline
- Automated deployment to AWS ECR + EC2
- Health checks and auto-restart

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, LangChain, Google Gemini, Pinecone
- **Frontend:** Jinja2, Tailwind CSS 
- **DevOps:** Docker, GitHub Actions, AWS (EC2, ECR)

---

## 📁 Project Structure

```
├── src/
│   ├── config.py          # Configuration
│   ├── helper.py          # Data processing
│   ├── prompt.py          # LLM prompts
│   └── utility.py         # Classifier & streaming
├── templates/
│   └── index.html         # UI
├── app.py                 # FastAPI app
├── store_index.py         # Vector store setup
├── Dockerfile             # Container config
└── .github/workflows/     # CI/CD pipeline
```

---

## 🌈 Architecture and Workflow Diagrams

<div align="center">

<img width="1361" height="753" alt="Screenshot 2025-12-12 082126" src="https://github.com/user-attachments/assets/e482ed2c-08e9-4b74-a076-41abbe5da50c" />

<img width="953" height="806" alt="Screenshot 2025-12-12 082207" src="https://github.com/user-attachments/assets/644fb50a-8c8d-41b1-9a12-3239c13dee74" />

<img width="475" height="841" alt="Screenshot 2025-12-12 082249" src="https://github.com/user-attachments/assets/5975b3e8-2aee-4420-ba85-dd8f2dbc553f" />

</div>

---

## 🚀 Setup & Deployment

**Want to run this project?**

👉 **[Complete Setup Instructions](SETUP.md)**

Includes local setup, Docker deployment, AWS deployment, and CI/CD configuration.

---

## 👤 Author

**Harsh Patel**  
📧 code.by.hp@gmail.com  
🔗 [GitHub](https://github.com/CodeBy-HP) • [LinkedIn](https://www.linkedin.com/in/harsh-patel-389593292/)

---

<div align="center">

**⭐ Star this repo if you find it useful**

</div>
