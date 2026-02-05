AI Task & Knowledge Assistant Backend

A production-style backend system that integrates Generative AI into task workflows and document understanding while maintaining security, reliability, and control.

🚀 Overview

This project is a FastAPI-based backend that combines:

Task management

AI-powered document Q&A (RAG)

Agent-based AI workflows

The system demonstrates how LLMs can be safely integrated into real applications with user isolation, execution control, and reliability safeguards.

🧩 Problem It Solves

Organizations want to use AI inside workflows but face challenges:

Hallucinated answers

Data leakage across users

Uncontrolled tool execution

Lack of observability

Unreliable AI behavior

This system provides a controlled AI backend that integrates LLMs into business logic safely.

⚙️ Features
Core Backend

FastAPI REST API

JWT Authentication

Role-based access control

Task CRUD APIs

Per-user data isolation

AI Capabilities

Retrieval-Augmented Generation (RAG)

Hybrid retrieval (vector + keyword/BM25)

Reranking for relevance

Agent workflow (Planner → Tools → Answer)

AI task prioritization endpoint

Reliability & Safety

Tool permission enforcement

Execution timeouts

Rate limiting

Hallucination & confidence scoring

Safety gate for unsupported answers

Observability via run logging (DB)

🧠 AI Architecture
Document Q&A Flow (RAG)

Upload → Chunk → Embed → Vector Store → Retrieve → Rerank → LLM Answer

Agent Workflow

User Prompt → Intent Classifier → Planner → Tool Execution → Final Answer

🔐 Security & Isolation

JWT-based authentication

Role-based tool permissions

Per-user vector store isolation

SQL and vector DB separation

Safety gate prevents unsupported responses

🗄 Tech Stack

FastAPI

SQLAlchemy

ChromaDB

LangChain

Groq LLM API

Pydantic

JWT



▶️ Run Locally
git clone <repo-url>
cd project
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload


Open Swagger:

http://127.0.0.1:8000/docs


create .env file 

DATABASE_URL=sqlite:///./app.db

# For production (PostgreSQL example)
# DATABASE_URL=postgresql://user:password@host:port/dbname

python -c "import secrets; print(secrets.token_urlsafe(64))"     # to check the secret key (paste this in terminal to get security key)
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256


ACCESS_TOKEN_EXPIRE_MINUTES=60

GROQ_API_KEY=your_groq_api_key_here

VECTOR_NAMESPACE=prod

AGENT_ENABLED=true
