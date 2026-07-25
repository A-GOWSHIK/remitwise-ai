# RemitWise AI – Backend

> **Agent-ready REST backend** for the RemitWise AI remittance advisory platform.
> AI agents built in NitroStack Studio consume these APIs to power intelligent remittance recommendations, compliance checks, and rate comparisons.

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
  - [Health](#health)
  - [Exchange Rates](#exchange-rates)
  - [Providers](#providers)
  - [Compliance](#compliance)
- [Data Sources](#data-sources)
- [Architecture Notes](#architecture-notes)
- [NitroStack Studio Integration](#nitrostack-studio-integration)

---

## Overview

RemitWise AI Backend provides three core capabilities:

| Domain | Data Source | Description |
|--------|-------------|-------------|
| **Exchange Rates** | Frankfurter API (live) | Mid-market rates, historical time-series, currency conversion |
| **Providers** | `data/providers.json` (local) | 5 major remittance providers with corridors, fees, and delivery methods |
| **Compliance** | `data/compliance_rules.json` (local) | KYC/AML rules, required documents, sanctions screening for 10 countries |

---

## Tech Stack

| Component | Library / Version |
|-----------|------------------|
| Language | Python 3.11+ |
| Framework | FastAPI 0.111 |
| Server | Uvicorn 0.30 |
| HTTP Client | Requests 2.32 |
| Validation | Pydantic v2 |
| Data | Local JSON + Frankfurter API |

---

## Project Structure

```
backend/
├── api/
│   ├── app.py                  ← FastAPI app, CORS, routers
│   └── routes/
│       ├── exchange.py         ← /exchange/* endpoints
│       ├── providers.py        ← /providers/* endpoints
│       ├── compliance.py       ← /compliance/* endpoints
│       └── health.py           ← /health endpoint
│
├── services/
│   ├── exchange_service.py     ← Frankfurter API wrapper
│   ├── provider_service.py     ← Provider data queries
│   └── compliance_service.py  ← Compliance rule queries
│
├── data/
│   ├── providers.json          ← 5 providers, corridors, fees
│   └── compliance_rules.json  ← 10 countries, KYC/AML rules
│
├── utils/
│   ├── file_loader.py          ← LRU-cached JSON reader
│   └── validators.py           ← Currency, country, date validators
│
├── config.py                   ← Centralised settings
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Clone / Navigate to project

```bash
cd backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the development server

```bash
# From the backend/ directory:
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

### 5. Explore the API

| URL | Description |
|-----|-------------|
| http://localhost:8000/docs | Swagger UI (interactive) |
| http://localhost:8000/redoc | ReDoc documentation |
| http://localhost:8000/health | Health check |
| http://localhost:8000/openapi.json | Raw OpenAPI schema |

---

## Environment Variables

All settings have sensible defaults so the server runs with zero configuration.

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |
| `RELOAD` | `true` | Hot-reload (disable in production) |
| `LOG_LEVEL` | `info` | Uvicorn log level |
| `CORS_ORIGINS` | `http://localhost:3000,...` | Comma-separated allowed origins |
| `FRANKFURTER_BASE_URL` | `https://api.frankfurter.app` | Exchange-rate API base URL |
| `HTTP_TIMEOUT_SECONDS` | `10` | Upstream API request timeout |

Create a `.env` file in `backend/` and export variables, or set them in your shell.

---

## API Reference

### Health

#### `GET /health`
Returns service liveness status.

```json
{
  "status": "ok",
  "service": "RemitWise AI Backend",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00+00:00",
  "uptime_seconds": 142.5
}
```

---

### Exchange Rates

All exchange-rate data is sourced live from the **Frankfurter API** (`https://api.frankfurter.app`).

#### `GET /exchange/latest`
Fetch the current exchange rate for a currency pair.

| Query Param | Type | Required | Example |
|-------------|------|----------|---------|
| `base` | string | ✅ | `USD` |
| `target` | string | ✅ | `INR` |

```bash
curl "http://localhost:8000/exchange/latest?base=USD&target=INR"
```

```json
{
  "base": "USD",
  "target": "INR",
  "rate": 83.45,
  "date": "2024-01-15",
  "amount": 1,
  "source": "Frankfurter API"
}
```

---

#### `GET /exchange/history`
Historical rates for a date range.

| Query Param | Type | Required | Example |
|-------------|------|----------|---------|
| `base` | string | ✅ | `USD` |
| `target` | string | ✅ | `INR` |
| `start_date` | string | ✅ | `2024-01-01` |
| `end_date` | string | ✅ | `2024-01-31` |

```bash
curl "http://localhost:8000/exchange/history?base=USD&target=INR&start_date=2024-01-01&end_date=2024-01-07"
```

```json
{
  "base": "USD",
  "target": "INR",
  "start_date": "2024-01-01",
  "end_date": "2024-01-07",
  "rates": {
    "2024-01-02": 83.12,
    "2024-01-03": 83.29
  },
  "count": 2,
  "source": "Frankfurter API"
}
```

---

#### `GET /exchange/convert`
Convert an amount between currencies.

| Query Param | Type | Required | Example |
|-------------|------|----------|---------|
| `base` | string | ✅ | `USD` |
| `target` | string | ✅ | `INR` |
| `amount` | float | ✅ | `1000.0` |

```bash
curl "http://localhost:8000/exchange/convert?base=USD&target=INR&amount=500"
```

---

#### `GET /exchange/currencies`
List all currencies supported by Frankfurter.

```bash
curl "http://localhost:8000/exchange/currencies"
```

---

### Providers

Provider data is served from `data/providers.json`.

#### `GET /providers`
List all active providers.

| Query Param | Type | Default | Description |
|-------------|------|---------|-------------|
| `active_only` | bool | `true` | Filter to active providers |

#### `GET /providers/corridors`
List transfer corridors across all providers.

| Query Param | Type | Required | Example |
|-------------|------|----------|---------|
| `from_country` | string | ❌ | `US` |
| `to_country` | string | ❌ | `IN` |

#### `GET /providers/compare`
Compare providers for a corridor.

| Query Param | Type | Required | Example |
|-------------|------|----------|---------|
| `from_country` | string | ✅ | `US` |
| `to_country` | string | ✅ | `IN` |

#### `GET /providers/{provider_id}`
Full details for a provider (e.g. `wise`, `remitly`, `western_union`).

#### `GET /providers/{provider_id}/payment-methods`
Accepted payment methods for a provider.

#### `GET /providers/{provider_id}/delivery-methods`
Delivery methods offered by a provider.

---

### Compliance

Compliance data is served from `data/compliance_rules.json`.

#### `GET /compliance`
Summary of all countries in the dataset.

#### `GET /compliance/{country}`
Full compliance profile for a country (e.g. `/compliance/US`, `/compliance/IN`).

#### `GET /compliance/{country}/documents`
Required and optional documents.

#### `GET /compliance/{country}/kyc`
KYC-specific requirements.

#### `GET /compliance/{country}/aml`
AML and sanctions screening requirements.

---

## Data Sources

### Frankfurter API
- **URL**: https://api.frankfurter.app
- **Auth**: None (free, public)
- **Rate limit**: ~unlimited for reasonable usage
- **Currencies**: EUR base + ~30 major currencies

### providers.json
Includes: **Wise**, **Remitly**, **Western Union**, **Sendwave**, **Xoom**

Fields per provider: id, name, corridors, payment methods, delivery methods, fees, transfer speed, compliance, rating.

### compliance_rules.json
Countries: **US, IN, GB, PH, MX, KE, NG, DE, CA, AU**

Fields: KYC/AML flags, sanctions screening, transaction limits, required documents, regulatory framework, risk level.

---

## Architecture Notes

- **Service layer** (`services/`) is completely decoupled from HTTP concerns. Services can be imported directly by NitroStack Studio agents without going through HTTP.
- **File caching** – JSON files are loaded once and cached in memory via `functools.lru_cache`. Call `reload_json_file()` to hot-reload without restart.
- **Validation** – All currency codes, country codes, and date inputs are validated before hitting services or external APIs.
- **Error handling** – Network errors, timeouts, and HTTP errors from Frankfurter are translated to appropriate HTTP status codes (502, 503, 504).

---

## NitroStack Studio Integration

The backend is designed for agent consumption:

1. **Base URL**: `http://localhost:8000` (or your deployed URL)
2. **OpenAPI Schema**: `GET /openapi.json` — import directly into NitroStack Studio
3. **No auth required** — add API key middleware when deploying to production
4. **Stateless** — all endpoints are stateless and safe to call concurrently
5. **JSON everywhere** — all responses are `application/json`

### Suggested agent tool bindings

| Agent Capability | Endpoint |
|-----------------|----------|
| Check current rate | `GET /exchange/latest` |
| Rate trend analysis | `GET /exchange/history` |
| Find best provider | `GET /providers/compare` |
| Check corridor support | `GET /providers/corridors` |
| Compliance screening | `GET /compliance/{country}` |
| Document checklist | `GET /compliance/{country}/documents` |
| KYC validation | `GET /compliance/{country}/kyc` |
