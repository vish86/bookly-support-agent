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

See the detailed instructions in the design document and backend/frontend READMEs (to be added in later tasks).

