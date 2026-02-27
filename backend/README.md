# Backend – Bookly Support Agent

This directory contains the Python FastAPI backend for the Bookly Support Agent.

## Features

- FastAPI application exposing:
  - `GET /health` – simple health check.
  - `POST /chat` – main agent interaction endpoint.
- Integration with OpenAI GPT-4o-mini via the official `openai` Python client.
- Functional, modular design:
  - `config.py` – environment-driven settings.
  - `schemas.py` – Pydantic models for requests/responses.
  - `llm_client.py` – thin wrapper around the OpenAI client.
  - `agent.py` – agent orchestration entry point (to be expanded with tools).
  - `main.py` – FastAPI app and routing.

## Installation

Create and activate a virtual environment, then install dependencies:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Set the following environment variables:

- `OPENAI_API_KEY` – your OpenAI API key.
- `OPENAI_MODEL` – optional, defaults to `gpt-4o-mini`.
- `OPENAI_TIMEOUT_SECONDS` – optional, request timeout in seconds (default: `20`).

You can place these in a `.env` file and load it via your preferred mechanism when running locally.

## Running the API

From the `backend` directory:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

- `GET http://localhost:8000/health` – health check.
- `POST http://localhost:8000/chat` – send a chat request with a list of messages.

