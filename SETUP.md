# 🚀 Setup Guide

## Prerequisites

- Python 3.10+
- API Keys: [Pinecone](https://www.pinecone.io/), [Google Gemini](https://makersuite.google.com/app/apikey)

---

## 🏠 Local Setup

### Clone Repository

```bash
git clone https://github.com/CodeBy-HP/Medical_Chatbot_LangChain.git
cd Medical_Chatbot_LangChain
```

### Create Virtual Environment

```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create `.env` file in root directory:

```env
PINECONE_API_KEY=your_pinecone_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Create Vector Store

If you have medical PDFs:

```bash
mkdir -p data
# Copy your PDF files to data/
python store_index.py
```

### Run Application

```bash
python app.py
```

Open: **http://localhost:8080**

---

## 🐳 Docker Setup

```bash
# Build
docker build -t medical-chatbot .

# Run
docker run -d -p 8080:8080 \
  -e PINECONE_API_KEY=your_key \
  -e GEMINI_API_KEY=your_key \
  --name medical-chatbot \
  medical-chatbot
```

---

## ☁️ Tech Stack

- Python 3.10
- FastAPI
- LangChain
- Google Gemini
- Pinecone
- Docker


---

## ☁️ AWS CI/CD Deployment

### 1. AWS Setup

**Create IAM User** with policies:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEC2FullAccess`

**Create ECR Repository:**
```bash
# Save the ECR URI for later
aws ecr create-repository --repository-name medical-chatbot
```

**Launch EC2 Instance:**
- Ubuntu 22.04 LTS
- t2.medium or larger
- Open port 8080 in security group

### 2. Configure EC2

SSH into EC2 and install Docker:

```bash
# Update system
sudo apt-get update -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

### 3. Setup Self-Hosted Runner

On GitHub: `Settings` → `Actions` → `Runners` → `New self-hosted runner`

Follow commands to configure runner on EC2.

### 4. Configure GitHub Secrets

Add these secrets in `Settings` → `Secrets and variables` → `Actions`:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
ECR_REPO
PINECONE_API_KEY
GEMINI_API_KEY
```

### 5. Deploy

Push to `main` branch → CI/CD pipeline automatically:
- Builds Docker image
- Pushes to ECR
- Deploys to EC2

---

