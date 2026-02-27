Bookly Support Agent
=====================

This project is a minimal but realistic customer support agent demo for **Bookly**, a fictional online bookstore.

The goal is to demonstrate thoughtful AI agent design rather than production-ready engineering.

## Overview

- **Frontend**: Single-page web app styled as a support console window using `shadcn/ui`.
- **Backend**: Python + FastAPI, integrating with OpenAI GPT-4o-mini.
- **Agent**: Formal, concise Bookly support representative.
- **Data**: High-quality synthetic data (orders, users, policies) held in memory; no persistence.

## Core Flows

- Order status inquiries (including delayed and problematic shipments).
- Return/refund requests with eligibility checks.
- General policy questions (shipping, refunds, password reset, etc.).

## Project Structure

- `backend/`: FastAPI app, agent orchestration, tools, synthetic data.
- `frontend/`: Next.js/React app using `shadcn/ui` for the UI.
- `docs/`: Design documents, including the one-page agent design.

## Running the Project

### 1. Backend (FastAPI + OpenAI)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."           # required
export OPENAI_MODEL="gpt-4o-mini"       # optional, defaults to gpt-4o-mini

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is then available at:

- `GET http://localhost:8000/health`
- `POST http://localhost:8000/chat`

### 2. Frontend (Bookly Support Console UI)

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser. The UI assumes the backend is reachable at `http://localhost:8000`.

### 3. Design Document

For the one-page AI agent design and more detail on architecture, prompts, tools, and productionization, see `docs/agent-design.md`.

