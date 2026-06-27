"""
Text preprocessing functions (lemmatization, stop words).
Identical to cell 2 of pipeline_final.ipynb.
"""
import re
import nltk
from nltk.corpus import stopwords as nltk_stopwords
from pymorphy3 import MorphAnalyzer
from functools import lru_cache

nltk.download("stopwords", quiet=True)

morph = MorphAnalyzer()
STOP_WORDS = set(nltk_stopwords.words("russian")) | {"г"}


@lru_cache(maxsize=4096)
def _lemmatize_token(token: str) -> str:
    return morph.parse(token)[0].normal_form


def preprocess(text: str) -> str:
    """Clean + lemmatize (mirrors preprocess_orgs from notebook)."""
    text = re.sub(r"[^\w\s]", " ", str(text).lower())
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [
        _lemmatize_token(t)
        for t in text.split()
        if t not in STOP_WORDS and len(t) > 1
    ]
    return " ".join(tokens)


def first_n_words(text: str, n: int = 6) -> str:
    return " ".join(str(text).split()[:n])


def prepare_text(course_name: str) -> str:
    """Full pipeline: raw -> speciality2 -> speciality3."""
    lemmatized = preprocess(course_name)
    return first_n_words(lemmatized, 6)
