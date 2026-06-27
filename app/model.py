"""
Singleton wrapper: loads TF-IDF vectorizer + HiClass LCPN model once on startup.
"""
import pickle
from pathlib import Path

_vectorizer = None
_model = None

MODEL_DIR = Path(__file__).parent.parent / "models"


def _load():
    global _vectorizer, _model
    if _vectorizer is None:
        with open(MODEL_DIR / "vectorizer.pkl", "rb") as f:
            _vectorizer = pickle.load(f)
    if _model is None:
        with open(MODEL_DIR / "hiclass_model.pkl", "rb") as f:
            _model = pickle.load(f)


def get_vectorizer():
    _load()
    return _vectorizer


def get_model():
    _load()
    return _model
