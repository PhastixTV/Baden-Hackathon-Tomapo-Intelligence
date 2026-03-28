# Tomapo Intelligence

ML-powered backend for food supply chain anomaly detection. Built for the Baden Hackathon.

Analyzes food shipment data from MongoDB `traces` documents using a hybrid approach: 17 rule-based checks combined with an Isolation Forest model. An integrated local LLM (Ollama) generates human-readable summaries and supports conversational analysis.

---

## Features

- **Anomaly Detection** — hybrid rule engine (17 checks across 9 categories) + Isolation Forest (28 features)
- **Risk Scoring** — 0–100 score mapped to `low / medium / high / critical` with automated recommendations
- **Sustainability Metrics** — CO2 per kg + eco-grade A–E
- **LLM Summary** — 2–3 sentence natural language batch summary via local Ollama model
- **Conversational Chat** — streaming chat endpoint with optional batch/product context, auto-detects German/English
- **Fully local** — no external AI APIs; all inference runs on-device via Ollama

---

## Architecture

```
app/
└── main.py              # FastAPI app — all endpoints and core logic

ml/
├── model.pkl            # Trained IsolationForest (200 estimators, 5% contamination)
├── feature_order.json   # 28 selected features used for inference
├── train.py             # Training script
└── generate_data.py     # Synthetic data generator (fish, meat, vegetables, beverages)

docs/
├── ml_fields.md         # Field definitions: MongoDB path, type, encoding (critical reference)
├── postman_test_bodies.md  # Ready-to-use Postman examples for all endpoints
├── schema-final.html    # Full MongoDB traces schema
└── datamodel-uml-5.html # UML diagram of the data model
```

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/analyze` | Analyze a food shipment — returns risk score, anomalies, sustainability, LLM summary |
| `POST` | `/chat` | Streaming conversational analysis with optional batch/product context |
| `GET` | `/health` | Health check |

### Risk Levels

| Score | Level | Recommendation |
|-------|-------|----------------|
| ≥ 76 | `critical` | `do_not_sell` |
| ≥ 51 | `high` | `quarantine` |
| ≥ 26 | `medium` | `inspect` |
| < 26 | `low` | `approve` |

---

## Anomaly Categories

The rule engine checks 9 categories:

- **Cold Chain** — temperature breaks, duration, pre-cooling failures
- **Temperature** — measured vs. allowed ranges (min/max)
- **Microbiology** — pathogen presence, CFU limits, listeria
- **Chemistry** — MRL violations, substance measurements
- **Laboratory** — verdict, accreditation, limit exceedances
- **Allergens** — detection, measurement, labeling correctness
- **Visual Inspection** — mold, foreign bodies, defect rate
- **Packaging** — leaks, sealing, vacuum, barcode, labeling
- **Traceability** — completeness, gaps, station verification

---

## Quick Start

### Prerequisites

- Python 3.11+
- Docker (for Ollama)

### Setup

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd Baden_Hackathon_Tomapo_Intelligence

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env if needed (default values work out of the box)
```

### Run (Development)

```bash
# Starts Ollama via Docker, pulls the model, then starts FastAPI with hot-reload
dev.bat
```

### Run (Production)

```bash
prod.bat
```

### Manual Start

```bash
# Start Ollama separately
docker compose up -d

# Pull the model
ollama pull llama3.2

# Start the API
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## Configuration

Copy `.env.example` to `.env` and adjust as needed:

```env
OLLAMA_MODEL=llama3.2
OLLAMA_HOST=http://localhost:11434
ML_MODEL_PATH=ml/model.pkl
ML_FEATURE_ORDER_PATH=ml/feature_order.json
```

---

## ML Model

The Isolation Forest is trained on 28 selected features (subset of ~90 total fields) to avoid the curse of dimensionality. Features cover cold chain, temperature, microbiology, chemistry, lab results, allergens, packaging, and traceability.

### Retrain the Model

```bash
# Generate synthetic training data
python ml/generate_data.py

# Train and save model + feature order
python ml/train.py
```

---

## Testing

Ready-made request bodies for all endpoints are in [`docs/postman_test_bodies.md`](docs/postman_test_bodies.md):

- Normal batch (meat — all green)
- High risk (fish — cold chain break)
- Critical (vegetables — multiple failures)
- Chat examples with and without product context

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI + Uvicorn |
| ML | scikit-learn (IsolationForest) |
| Data | pandas, numpy, scipy |
| LLM | Ollama (llama3.2, local) |
| Validation | Pydantic v2 |
| Containerization | Docker Compose |
| Config | python-dotenv |
