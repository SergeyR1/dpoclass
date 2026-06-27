# 🎓 dpoclass — Course Classifier API

Иерархическая классификация названий курсов педагогов по 4 уровням.  
Модель: **HiClass LCPN** (LocalClassifierPerNode) + **RandomForest** + **TF-IDF** (биграммы).  
Обучена на ~20 000 вручную размеченных программ ДПО (повышение квалификации и профессиональная переподготовка).

🔗 Репозиторий: https://github.com/SergeyR1/dpoclass

## Структура репозитория

```
dpoclass/
├── app/
│   ├── main.py            # FastAPI приложение (эндпоинты)
│   ├── classifier.py      # Бизнес-логика классификации
│   ├── model.py           # Singleton-загрузчик модели
│   └── preprocessing.py   # Лемматизация и препроцессинг текста
├── models/
│   ├── hiclass_model.pkl  # Обученная HiClass-модель (скачать из Releases)
│   └── vectorizer.pkl     # TF-IDF векторизатор (скачать из Releases)
├── data/
│   └── classifier-2.csv   # Справочник классификатора (lvl1–lvl4)
├── tests/
│   └── test_api.py        # Pytest-тесты эндпоинтов
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Быстрый старт

### Вариант А: локально

**1. Клонировать репозиторий и установить зависимости**

```bash
git clone https://github.com/SergeyR1/dpoclass.git
cd dpoclass
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**2. Скачать файлы модели**

Скачайте `vectorizer.pkl` и `hiclass_model.pkl` из раздела [Releases](https://github.com/SergeyR1/dpoclass/releases)  
и положите их в папку `models/`.

**3. Запустить API**

```bash
uvicorn app.main:app --reload
```

API: http://localhost:8000  
Swagger UI: http://localhost:8000/docs

---

### Вариант Б: Docker (зависимости не нужны)

**1. Клонировать репозиторий**

```bash
git clone https://github.com/SergeyR1/dpoclass.git
cd dpoclass
```

**2. Скачать файлы модели**

Скачайте `vectorizer.pkl` и `hiclass_model.pkl` из раздела [Releases](https://github.com/SergeyR1/dpoclass/releases)  
и положите их в папку `models/`.

**3. Запустить**

```bash
docker compose up --build
```

API: http://localhost:8000

---

## Использование API

### POST /classify

Классификация одного курса:

```bash
curl -X POST http://localhost:8000/classify \
     -H "Content-Type: application/json" \
     -d '{"course_name": "Организация инклюзивного образования в школе"}'
```

Ответ:

```json
{
  "input": "Организация инклюзивного образования в школе",
  "lvl1": "Образование и педагогические науки",
  "lvl2": "Педагогическое образование",
  "lvl3": "Основное и среднее общее образование",
  "lvl4": "остальное4"
}
```

### POST /classify/batch

Классификация нескольких курсов (до 100 за раз):

```bash
curl -X POST http://localhost:8000/classify/batch \
     -H "Content-Type: application/json" \
     -d '[{"course_name": "Математика"}, {"course_name": "Охрана труда"}]'
```

### GET /health

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

## Справочник классификатора

Файл `data/classifier-2.csv` содержит все допустимые комбинации меток lvl1–lvl4  
(разделитель `;`).

| Поле | Описание |
|------|----------|
| lvl1 | Область знаний (например, «Образование и педагогические науки») |
| lvl2 | Направление (например, «Педагогическое образование») |
| lvl3 | Специализация (например, «Дошкольное образование») |
| lvl4 | Предмет или профиль (например, «Математика») |

## Тесты

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

## Зависимости

| Пакет | Назначение |
|-------|-----------|
| `hiclass` | Иерархическая классификация (LCPN) |
| `scikit-learn` | RandomForest, TF-IDF |
| `pymorphy3` | Морфологический анализ русского текста |
| `fastapi` | REST API фреймворк |
| `uvicorn` | ASGI-сервер |

## Лицензия

Apache 2.0
