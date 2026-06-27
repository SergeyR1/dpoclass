# 🎓 dpoclass — Course Classifier API

Hierarchical classification of teacher course names across 4 levels.  
Model: **HiClass LCPN** (LocalClassifierPerNode) + **RandomForest** + **TF-IDF** (bigrams).  
Trained on ~20,000 manually labeled professional development (CPD) programs.

🔗 Repository: https://github.com/SergeyR1/dpoclass

## Repository Structure

```
dpoclass/
├── app/
│   ├── main.py            # FastAPI application (endpoints)
│   ├── classifier.py      # Classification business logic
│   ├── model.py           # Singleton model loader
│   └── preprocessing.py   # Russian text lemmatization & preprocessing
├── models/
│   ├── hiclass_model.pkl  # Trained HiClass model (download from Releases)
│   └── vectorizer.pkl     # TF-IDF vectorizer (download from Releases)
├── data/
│   └── classifier-2.csv   # Classifier reference dictionary (lvl1–lvl4)
├── tests/
│   └── test_api.py        # Pytest endpoint tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Quick Start

### Option A: Local

**1. Clone and install dependencies**

```bash
git clone https://github.com/SergeyR1/dpoclass.git
cd dpoclass
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**2. Download model files**

Download `vectorizer.pkl` and `hiclass_model.pkl` from [Releases](https://github.com/SergeyR1/dpoclass/releases)  
and place them in the `models/` folder.

**3. Start the API**

```bash
uvicorn app.main:app --reload
```

API: http://localhost:8000  
Swagger UI: http://localhost:8000/docs

---

### Option B: Docker (no local dependencies needed)

**1. Clone the repository**

```bash
git clone https://github.com/SergeyR1/dpoclass.git
cd dpoclass
```

**2. Download model files**

Download `vectorizer.pkl` and `hiclass_model.pkl` from [Releases](https://github.com/SergeyR1/dpoclass/releases)  
and place them in the `models/` folder.

**3. Run**

```bash
docker compose up --build
```

API: http://localhost:8000

---

## API Usage

### POST /classify

```bash
curl -X POST http://localhost:8000/classify \
     -H "Content-Type: application/json" \
     -d '{"course_name": "Inclusive education in secondary schools"}'
```

Response:

```json
{
  "input": "Inclusive education in secondary schools",
  "lvl1": "Образование и педагогические науки",
  "lvl2": "Педагогическое образование",
  "lvl3": "Основное и среднее общее образование",
  "lvl4": "остальное4"
}
```

### POST /classify/batch

Classify up to 100 courses in a single request:

```bash
curl -X POST http://localhost:8000/classify/batch \
     -H "Content-Type: application/json" \
     -d '[{"course_name": "Mathematics"}, {"course_name": "Labor safety"}]'
```

### GET /health

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

## Classifier Reference Dictionary

`data/classifier-2.csv` lists all valid label combinations for lvl1–lvl4 (semicolon-delimited).

| Field | Description |
|-------|-------------|
| lvl1  | Knowledge domain (e.g., "Education and Pedagogical Sciences") |
| lvl2  | Direction (e.g., "Pedagogical Education") |
| lvl3  | Specialization (e.g., "Pre-school Education") |
| lvl4  | Subject or profile (e.g., "Mathematics") |

## Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `hiclass` | Hierarchical classification (LCPN) |
| `scikit-learn` | RandomForest, TF-IDF |
| `pymorphy3` | Russian morphological analysis |
| `fastapi` | REST API framework |
| `uvicorn` | ASGI server |

## License

MIT
