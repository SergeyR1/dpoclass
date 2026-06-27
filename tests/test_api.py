"""
Basic FastAPI endpoint tests.
Run: pytest tests/
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

MOCK_PREDICTION = [
    ["Образование и педагогические науки", "Педагогическое образование",
     "Дошкольное образование", "остальное4"]
]


@pytest.fixture(scope="module")
def client():
    mock_vec = MagicMock()
    mock_vec.transform.return_value.toarray.return_value = [[0.1] * 10]
    mock_model = MagicMock()
    mock_model.predict.return_value = MOCK_PREDICTION

    with patch("app.model.get_vectorizer", return_value=mock_vec), \
         patch("app.model.get_model", return_value=mock_model):
        from app.main import app
        yield TestClient(app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_classify_returns_four_levels(client):
    r = client.post("/classify", json={"course_name": "Дошкольное образование для воспитателей"})
    assert r.status_code == 200
    data = r.json()
    for key in ["lvl1", "lvl2", "lvl3", "lvl4", "input"]:
        assert key in data


def test_classify_empty_raises(client):
    r = client.post("/classify", json={"course_name": " "})
    assert r.status_code == 422


def test_batch_classify(client):
    payload = [{"course_name": "Математика"}, {"course_name": "Физика"}]
    r = client.post("/classify/batch", json=payload)
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_batch_limit(client):
    payload = [{"course_name": f"Курс {i}"} for i in range(101)]
    r = client.post("/classify/batch", json=payload)
    assert r.status_code == 400
