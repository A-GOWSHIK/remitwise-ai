# 🌍 RemitWise AI — Multi-Agent Cross-Border Remittance Advisor

[![NitroStack](https://img.shields.io/badge/Built_With-NitroStack_MCP-8A2BE2.svg)](https://github.com/A-GOWSHIK/remitwise-ai)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](docs/LICENSE)
[![Status](https://img.shields.io/badge/Status-Hackathon_MVP-brightgreen.svg)](https://github.com/A-GOWSHIK/remitwise-ai)

RemitWise AI is an intelligent, production-quality multi-agent platform developed for the **NitroStack × Amrita University Hackathon**. It helps users make optimal international money transfer decisions by combining live exchange rates, multi-provider fee comparisons, automated KYC/AML compliance verification, rate timing predictions, and interactive transfer tracking.

Built using **FastAPI**, **NitroStack SDK**, **Model Context Protocol (MCP)**, **Ollama Llama 3.1**, and **React 19 + TypeScript**.

---

## 👥 Team Members & GitHub Identifiers

- **A-GOWSHIK**: [@A-GOWSHIK](https://github.com/A-GOWSHIK) (Lead Developer)
- **vijay45057**: [@vijay45057](https://github.com/vijay45057) (Core Contributor)
- **Kavin-2806**: [@Kavin-2806](https://github.com/Kavin-2806) (Core Contributor)

🔗 **Official GitHub Repository**: [https://github.com/A-GOWSHIK/remitwise-ai.git](https://github.com/A-GOWSHIK/remitwise-ai.git)

---

## 🎥 Project Demo Video

> 📺 **Demo Video**: *[Link to 3-Minute Video Demo - Explaining Problem Statement, Solution Architecture, and Working Demonstration]*

---

## 🏗️ System Architecture & Multi-Agent Design

RemitWise AI uses a specialized multi-agent orchestrator architecture:

1. **OrchestratorAgent**: Classifies natural language intent, creates step-by-step execution plans, and dispatches sub-agent tasks.
2. **ExchangeAgent**: Connects to the live Frankfurter API for mid-market FX rates, historical trends, and timing prediction.
3. **ProviderAgent**: Queries 5 major remittance providers (Wise, Remitly, Western Union, Revolut, OFX) to compare net payouts and fees.
4. **ComplianceAgent**: Validates corridor regulations, daily transaction caps, and required KYC documents across 10 countries.
5. **Results Merger Engine**: Aggregates sub-agent data, calculates savings metrics, and returns a unified JSON response payload to the UI or MCP client.

---

## 🚀 Quick Start Guide

### 1. Install & Serve Ollama (Primary LLM Engine)

RemitWise AI uses **Ollama** with the `llama3.1` model by default for natural language planning.

```bash
# Pull the recommended model
ollama pull llama3.1

# Start the Ollama server (default host: http://localhost:11434)
ollama serve
```

### 2. Run the Backend Service (FastAPI)

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

# Launch FastAPI server
python -m uvicorn api.app:app --reload
```
The backend server will be available at `http://localhost:8000` (Swagger docs at `http://localhost:8000/docs`).

### 3. Run the Frontend Dashboard (React + Vite)

```bash
cd frontend

# Install Node dependencies
npm install

# Start development server
npm run dev
```
The frontend UI will be available at `http://localhost:5173`.

---

## 🛡️ Multi-Tier Automatic Fallback Mechanics

The multi-agent system features a resilient, 3-tier fallback architecture to ensure **zero downtime** and **100% operational availability**:

```
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
2. **Fallback 1 (`MockProvider`)**: If Ollama is offline or unavailable, automatically switches to `MockProvider` without raising errors.
3. **Fallback 2 (`RuleBasedPlanner`)**: If LLM planning fails completely, automatically falls back to deterministic rule-based planning.

> **Note**: The application will **never crash** due to an LLM service failure or network timeout.

---

## ⚙️ Configuration Guide

Set configuration variables in `backend/.env` or system environment:

```bash
# Default provider settings
LLM_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1

# Optional OpenAI Provider settings
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

---

## 🧪 Running Tests

```bash
cd backend

# Run the complete test suite (64 passing unit & integration tests)
python -m pytest tests/ -v
```

---

## 📚 Complete Project Documentation (`docs/`)

Detailed documentation is available in the [`docs/`](docs/) directory:

- 📐 **[System Architecture](docs/architecture/system-architecture.md)**: Architectural blueprint, component responsibilities, and data flow.
- 📡 **[API Reference](docs/api.md)**: Complete REST API endpoint documentation and MCP Server tools.
- 🔄 **[Workflow Specification](docs/workflow.md)**: End-to-end execution flow from user query to UI rendering.
- 📝 **[Changelog](docs/CHANGELOG.md)**: Release notes for v1.0.0 Hackathon MVP.
- 🤝 **[Contributing Guidelines](docs/CONTRIBUTING.md)**: Team contribution standards and Git security rules.
- 📄 **[License](docs/LICENSE)**: Official MIT License.

---

## 📜 License

Distributed under the **MIT License**. See [`docs/LICENSE`](docs/LICENSE) for more details.
