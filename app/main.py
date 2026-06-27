"""
FastAPI application — course classifier (HiClass LCPN + TF-IDF).
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.classifier import classify

app = FastAPI(
    title="Course Classifier API",
    description=(
        "Hierarchical classification of teacher course names "
        "across 4 levels (HiClass LCPN + RandomForest + TF-IDF). "
        "Model trained with HiClass LCPN + RandomForest + TF-IDF on ~20k CPD programs."
    ),
    version="1.0.0",
)


# ── Schemas ─────────────────────────────────────────────────────────────────

class ClassifyRequest(BaseModel):
    course_name: str = Field(
        ...,
        min_length=2,
        max_length=500,
        example="Организация инклюзивного образования в школе",
    )


class ClassifyResponse(BaseModel):
    input: str
    lvl1: str
    lvl2: str
    lvl3: str
    lvl4: str


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Course Classifier API is running"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.post("/classify", response_model=ClassifyResponse, tags=["Classify"])
def classify_course(request: ClassifyRequest):
    """
    Classify a course name into a 4-level hierarchy lvl1 -> lvl2 -> lvl3 -> lvl4.

    - **course_name**: raw course or CPD program name
    """
    try:
        result = classify(request.course_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")
    return ClassifyResponse(**result)


@app.post("/classify/batch", response_model=list[ClassifyResponse], tags=["Classify"])
def classify_batch(requests: list[ClassifyRequest]):
    """
    Classify multiple courses in a single request (up to 100).
    """
    if len(requests) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 courses per request")
    results = []
    for req in requests:
        try:
            results.append(classify(req.course_name))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model error: {e}")
    return [ClassifyResponse(**r) for r in results]
