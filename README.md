# 🌍 RemitWise AI — Multi-Agent Cross-Border Remittance Advisor

[![NitroStack](https://img.shields.io/badge/Built_With-NitroStack_MCP-8A2BE2.svg)](https://github.com/A-GOWSHIK/remitwise-ai)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](docs/LICENSE)
[![Status](https://img.shields.io/badge/Status-Hackathon_MVP-brightgreen.svg)](https://github.com/A-GOWSHIK/remitwise-ai)

RemitWise AI is an intelligent, production-quality multi-agent platform developed for the **NitroStack × Amrita University Hackathon** by **Team Sambar Spartans**. It helps users make optimal international money transfer decisions by combining **live exchange rates**, **multi-provider fee comparisons**, **automated KYC/AML compliance verification**, **rate timing predictions**, and **interactive transfer tracking**.

Built using **FastAPI**, **NitroStack SDK**, **Model Context Protocol (MCP)**, **Ollama Llama 3.1**, and **React 19 + TypeScript**.

---

## 👥 Team Members & Project Information

- **Team Name**: **Sambar Spartans**
- **Hackathon**: **NitroStack × Amrita University Hackathon**
- **Project**: **RemitWise AI**
- **Official GitHub Repository**: [https://github.com/A-GOWSHIK/remitwise-ai.git](https://github.com/A-GOWSHIK/remitwise-ai.git)

### Team Members
1. **A-GOWSHIK** — [@A-GOWSHIK](https://github.com/A-GOWSHIK) 
2. **vijay45057** — [@vijay45057](https://github.com/vijay45057) 
3. **Kavin-2806** — [@Kavin-2806](https://github.com/Kavin-2806) 

---

## 🎥 Project Demo Video

> 📺 **Demo Video**: *[Link to 3-Minute Video Demo - Explaining Problem Statement, Solution Architecture, and Working Demonstration]*

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Powered by NitroStack](#-powered-by-nitrostack)
- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Why RemitWise AI?](#-why-remitwise-ai)
- [Key Features](#-key-features)
- [Multi-Agent System Architecture](#-multi-agent-system-architecture)
- [3-Tier Automatic Fallback Mechanics](#-3-tier-automatic-fallback-mechanics)
- [System Workflow](#-system-workflow)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Quick Start & Installation](#-quick-start--installation)
- [Environment Variables](#-environment-variables)
- [Running Tests](#-running-tests)
- [Project Documentation](#-project-documentation-docs)
- [License](#-license)

---

## 📖 Project Overview

International money transfers often involve multiple providers, fluctuating exchange rates, hidden transfer fees, and complex country-specific compliance requirements.

RemitWise AI simplifies this process using a modular **Multi-Agent System Architecture**. Instead of relying on a single monolithic model or static form lookup, specialized AI agents independently retrieve live exchange rates, compare remittance providers, verify compliance requirements, and generate intelligent, transparent recommendations.

---

## 🚀 Powered by NitroStack

RemitWise AI is built on **NitroStack's Model Context Protocol (MCP)**.

NitroStack serves as the AI orchestration layer of our application by enabling multiple specialized AI agents to work together as a unified intelligent system.

### NitroStack Core Responsibilities
- AI Agent orchestration & dynamic routing
- Model Context Protocol (MCP) server integration
- Inter-agent communication & data synthesis
- MCP Tool execution & schema validation
- Modular AI workflow execution

---

## ❗ Problem Statement

Cross-border money transfers are challenging because:
- **Rate Volatility**: Mid-market exchange rates change constantly.
- **Opaque Fees**: Transfer fees and exchange rate margins vary wildly across providers.
- **Complex Compliance**: KYC/AML rules and document requirements differ between countries.
- **Manual Overhead**: Finding the best rate and fee combination requires searching multiple websites manually.

Most existing platforms only display exchange rates or fixed lists without intelligent decision support.

---

## 💡 Our Solution

RemitWise AI solves these challenges with specialized agents working in tandem:

- 🧠 **Planner / Orchestrator Agent**: Analyzes user intent and coordinates execution.
- 💱 **Exchange Agent**: Fetches live mid-market rates (Frankfurter API) and time-series trends.
- 🏦 **Provider Agent**: Compares 5 major providers (Wise, Remitly, Western Union, Revolut, OFX) on fees, speed, and net payout.
- 🛡️ **Compliance Agent**: Validates KYC/AML guidelines and transfer caps for 10 countries.
- 🔄 **Merger Engine**: Combines all outputs into a single, unified AI recommendation.

---

## 🌟 Why RemitWise AI?

Unlike conventional remittance portals, RemitWise AI acts as an **intelligent financial advisory assistant**. Users receive:
- **Net Payout Optimization**: Clear breakdown of which provider gives the maximum recipient amount.
- **Timing Prediction**: Rate trend confidence meter advising whether to transfer now or hold.
- **Instant Compliance Verification**: Precise list of required KYC documents per corridor.
- **Zero-Downtime Resilience**: 3-tier automatic fallback system.

---

## ✨ Key Features

### 🤖 AI & Multi-Agent Intelligence
- Dynamic natural language planning using Ollama (`llama3.1`)
- Multi-tier resilient LLM fallback engine
- Unified payload merging and savings counter calculation

### 💱 Remittance & Provider Analytics
- Live mid-market FX rates with LRU caching
- 5-Provider comparison matrix (Wise, Remitly, Western Union, Revolut, OFX)
- Payout amount, effective rate, transfer fee, and delivery time breakdown

### 🛡️ Regulation & Compliance
- Automated corridor limit validation across 10 countries
- KYC document requirements (Tier 1 & Tier 2)

### 💻 Modern Web UI
- React 19 + TypeScript + Vite dashboard
- Interactive Recharts rate trends & Framer Motion micro-animations
- Live rate ticker bar

---

## 🏗️ Multi-Agent System Architecture

```text
                               ┌────────────────────────┐
                               │     User Query / UI    │
                               └───────────┬────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │   OrchestratorAgent    │
                               │    (Planner Engine)    │
                               └───────────┬────────────┘
                                           │ Dynamic Task Delegation
                     ┌─────────────────────┼─────────────────────┐
                     ▼                     ▼                     ▼
           ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
           │  ExchangeAgent   │  │  ProviderAgent   │  │ ComplianceAgent  │
           │(Frankfurter API) │  │  (5 Providers)   │  │ (10 Regulations) │
           └─────────┬────────┘  └─────────┬────────┘  └─────────┬────────┘
                     │                     │                     │
                     └─────────────────────┼─────────────────────┘
                                           │ Sub-agent Data
                                           ▼
                               ┌────────────────────────┐
                               │     Merger Engine      │
                               └───────────┬────────────┘
                                           │ Unified Advisory Payload
                                           ▼
                               ┌────────────────────────┐
                               │  React 19 Dashboard UI │
                               └────────────────────────┘
```

---

## 🛡️ 3-Tier Automatic Fallback Mechanics

The multi-agent system features a resilient, 3-tier fallback architecture to ensure **zero downtime** and **100% operational availability**:

```text
                       User Request
                            │
                            ▼
                  OrchestratorAgent
                            │
            ┌───────────────┴───────────────┐
            │   Primary LLM: OllamaProvider │
            │   (Host: localhost:11434)     │
            └───────────────┬───────────────┘
                            │ (If offline / connection refused / model missing / timeout)
                            ▼
            ┌───────────────────────────────┐
            │  Fallback 1: MockProvider     │
            │  (Offline simulation)         │
            └───────────────┬───────────────┘
                            │ (If LLM response malformed / invalid)
                            ▼
            ┌───────────────────────────────┐
            │  Fallback 2: RuleBasedPlanner │
            │  (Deterministic Heuristics)   │
            └───────────────────────────────┘
```

1. **Primary (`OllamaProvider`)**: Attempts connection to local Ollama (`llama3.1`).
2. **Fallback 1 (`MockProvider`)**: If Ollama is offline or unavailable, automatically switches to `MockProvider`.
3. **Fallback 2 (`RuleBasedPlanner`)**: If LLM response fails validation, falls back to deterministic keyword planning.

> **Zero Downtime**: The backend will never crash due to an LLM service outage or network failure.

---

## 🔄 System Workflow

```text
User submits remittance request
            │
            ▼
Orchestrator analyzes intent & plans execution
            │
            ▼
Specialist agents execute concurrently (Exchange + Provider + Compliance)
            │
            ▼
Raw data collected from Live APIs & Datasets
            │
            ▼
Merger Engine aggregates & calculates savings metrics
            │
            ▼
Unified AI recommendation returned to UI / MCP Client
```

---

## 🛠️ Technology Stack

| Domain | Technology |
|--------|------------|
| **Frontend** | React 19, TypeScript, Vite 8, TailwindCSS 4, Framer Motion, Recharts |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, Pydantic v2, Requests |
| **AI Architecture** | Multi-Agent Orchestrator, Ollama (`llama3.1`), MockProvider, RuleBasedPlanner |
| **Protocol** | Model Context Protocol (MCP), NitroStack SDK |
| **Live FX API** | Frankfurter Exchange API |
| **Testing** | Pytest, Pytest-Asyncio (64 tests passing) |
| **Version Control** | Git, GitHub |

---

## 📂 Project Structure

```text
remitwise-ai/
├── backend/
│   ├── agents/              # AI specialist agents (Exchange, Provider, Compliance, Orchestrator)
│   ├── api/                 # FastAPI routes & app entry point
│   ├── data/                # Provider data & compliance rules JSON
│   ├── services/            # Core business logic services
│   ├── tests/               # 64 automated unit & integration tests
│   ├── utils/               # LRU cache & validators
│   ├── config.py            # Centralized settings
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── public/              # Static assets
│   ├── src/                 # React components, hooks, contexts
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
│
├── docs/
│   ├── architecture/        # System architecture blueprints
│   ├── screenshots/         # UI screenshot documentation
│   ├── .env.example         # Environment template
│   ├── api.md               # REST API & MCP documentation
│   ├── workflow.md          # Multi-agent workflow spec
│   ├── CHANGELOG.md         # Release history
│   ├── CONTRIBUTING.md      # Team contribution rules
│   └── LICENSE              # MIT License
│
├── AGENTS.md
├── README.md
└── .gitignore
```

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/A-GOWSHIK/remitwise-ai.git
cd remitwise-ai
```

### 2. Start Ollama (Primary LLM Engine)
```bash
# Pull model
ollama pull llama3.1

# Start server
ollama serve
```

### 3. Launch Backend API
```bash
cd backend

# Create & activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI dev server
python -m uvicorn api.app:app --reload
```
Backend API will run at `http://localhost:8000` (Swagger UI: `http://localhost:8000/docs`).

### 4. Launch Frontend UI
```bash
cd frontend

# Install Node modules
npm install

# Start Vite dev server
npm run dev
```
Frontend UI will run at `http://localhost:5173`.

---

## ⚙️ Environment Variables

Copy [.env.example](docs/.env.example) to `.env` in the `backend/` directory:

```env
# Backend Server
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# LLM Config
LLM_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1
```

---

## 🧪 Running Tests

```bash
cd backend

# Run full test suite (64 passing tests)
python -m pytest tests/ -v
```

---

## 📚 Project Documentation (`docs/`)

Detailed documentation is available in the [`docs/`](docs/) directory:

- 📐 **[System Architecture](docs/architecture/system-architecture.md)**: Architectural blueprint, agent roles, and data flow.
- 📡 **[API Reference](docs/api.md)**: REST endpoints and MCP Server tools.
- 🔄 **[Workflow Specification](docs/workflow.md)**: Step-by-step execution flow.
- 📝 **[Changelog](docs/CHANGELOG.md)**: Version history for v1.0.0 Hackathon MVP.
- 🤝 **[Contributing Guidelines](docs/CONTRIBUTING.md)**: Contribution guidelines and Git security rules.
- 📄 **[License](docs/LICENSE)**: Official MIT License.

---

## 📜 License

Distributed under the **MIT License**. See [`docs/LICENSE`](docs/LICENSE) for more information.
