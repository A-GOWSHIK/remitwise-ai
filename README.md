# 🌍 RemitWise AI

### AI-Powered Multi-Agent Cross-Border Remittance Advisor

RemitWise AI is an intelligent multi-agent platform that helps users make informed international money transfer decisions by combining **live exchange rates**, **provider comparison**, **compliance verification**, and **AI-powered recommendations**.

Built using **FastAPI**, **NitroStack**, **Model Context Protocol (MCP)**, and a modular **Multi-Agent Architecture**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![NitroStack](https://img.shields.io/badge/NitroStack-MCP-orange)
![License](https://img.shields.io/badge/License-MIT-red)
![Status](https://img.shields.io/badge/Status-Production-success)

---

# 📑 Table of Contents

- Project Overview
- Problem Statement
- Our Solution
- Why RemitWise AI?
- Features
- Multi-Agent Architecture
- System Workflow
- Technology Stack
- Project Structure

---

# 📖 Project Overview

International remittances often involve multiple providers, fluctuating exchange rates, hidden transfer fees, and country-specific compliance requirements.

RemitWise AI simplifies this process using a modular multi-agent architecture. Instead of relying on a single AI model, specialized agents independently retrieve exchange rates, compare remittance providers, verify compliance requirements, and generate intelligent recommendations.

The platform delivers transparent, real-time insights before users initiate international money transfers, helping them make faster and more informed financial decisions.

---

# ❗ Problem Statement

Cross-border money transfers are often difficult because:

- Exchange rates change frequently.
- Transfer fees vary across providers.
- Compliance requirements differ between countries.
- Users lack transparent provider comparisons.
- Choosing the best transfer option requires manual research.

Most existing platforms only solve part of the problem by displaying exchange rates or transfer options without providing intelligent decision support.

---

# 💡 Our Solution

RemitWise AI addresses these challenges through a modular multi-agent system.

Each specialized AI agent performs an independent task before the final response is generated.

### Planner Agent

- Understands the user's request
- Determines which specialist agents are required

### Exchange Agent

- Retrieves live exchange rates
- Performs currency conversion

### Provider Agent

- Compares remittance providers
- Evaluates fees
- Compares transfer speed
- Analyzes payout methods

### Compliance Agent

- Verifies KYC requirements
- Checks AML rules
- Reviews sanctions information

### Merger Agent

- Combines outputs from every specialist agent
- Produces one unified recommendation

---

# 🌟 Why RemitWise AI?

Unlike conventional remittance platforms that only display exchange rates or provider information, RemitWise AI acts as an intelligent decision-support assistant.

Instead of searching across multiple websites, users receive:

- Live exchange rate information
- Provider comparison
- Compliance guidance
- AI-generated recommendations

All generated through a coordinated multi-agent workflow.

---

# ✨ Features

## 🤖 AI & Multi-Agent System

- Intelligent Planner Agent
- Modular Specialist Agents
- Automatic Provider Fallback
- AI-Powered Recommendations

## 💱 Remittance Intelligence

- Live Exchange Rates
- Currency Conversion
- Provider Comparison
- Compliance Verification

## ⚙️ Platform

- FastAPI Backend
- React + NitroStack Frontend
- RESTful APIs
- MCP Integration
- Render Deployment
- Modular Architecture

---

# 🏗️ Multi-Agent Architecture

The platform follows a modular architecture where an intelligent planner coordinates multiple specialist agents.

- **Planner Agent** — Analyzes the user's request and selects the required agents.
- **Exchange Agent** — Retrieves live exchange rates and performs currency conversion.
- **Provider Agent** — Compares remittance providers based on fees, transfer speed, payout methods, and exchange rates.
- **Compliance Agent** — Validates KYC, AML, sanctions, and transfer requirements.
- **Merger Agent** — Combines all outputs into a single response.

> **Architecture diagram will be added here**

```text
                 User Query
                      │
                      ▼
              Planner Agent
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
Exchange Agent   Provider Agent   Compliance Agent
      │               │                │
      └───────────────┼────────────────┘
                      ▼
                Merger Agent
                      ▼
          Final AI Recommendation
```

---

# 🔄 System Workflow

The following workflow describes how a user request is processed.

```text
User submits remittance request
            │
            ▼
Planner analyzes user intent
            │
            ▼
Required specialist agents execute
            │
            ▼
Exchange + Provider + Compliance data collected
            │
            ▼
Merger Agent combines all responses
            │
            ▼
Final recommendation returned
```

Workflow Summary

1. User submits a remittance query.
2. Planner Agent analyzes the request.
3. Specialist agents execute independently.
4. Results are merged.
5. A unified response is presented to the user.

---

# 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Frontend | React, TypeScript, NitroStack |
| Backend | Python, FastAPI |
| AI Architecture | Multi-Agent System |
| Protocol | Model Context Protocol (MCP) |
| APIs | Frankfurter Exchange API |
| LLM Support | Ollama, Mock Provider |
| Deployment | Render, NitroCloud |
| Version Control | Git, GitHub |

---

# 📂 Project Structure

```text
remitwise-ai/
│
├── backend/
│   ├── agents/              # AI specialist agents
│   ├── api/                 # FastAPI routes
│   ├── data/                # Data files
│   ├── services/            # Business logic
│   ├── tests/               # Test cases
│   ├── utils/               # Utility functions
│   ├── config.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
│
├── docs/
│   ├── architecture/
│   ├── screenshots/
│   ├── api.md
│   └── workflow.md
│
├── .env.example
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── .gitignore
```

---

> **The following sections will be added in the next phase:**
>
> - ⚙️ Prerequisites
> - 📥 Installation
> - 🔐 Environment Variables
> - ▶️ Running the Project
> - 🌐 API Documentation
> - ☁️ Deployment
> - 📸 Screenshots
> - 🎥 Demo
> - 🚀 Future Enhancements
> - 👥 Contributors
> - 📄 License
