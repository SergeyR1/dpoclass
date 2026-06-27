"""
Classification business logic for a single course.
"""
from app.model import get_vectorizer, get_model
from app.preprocessing import prepare_text

LEVEL_COLS = ["lvl1", "lvl2", "lvl3", "lvl4"]


def classify(course_name: str) -> dict:
    """
    Accept a course name, return dict with lvl1-lvl4.

    Parameters
    ----------
    course_name : str
        Raw course / program name.

    Returns
    -------
    dict  {lvl1, lvl2, lvl3, lvl4, input}
    """
    vec = get_vectorizer()
    model = get_model()

    text = prepare_text(course_name)
    X = vec.transform([text]).toarray()
    prediction = model.predict(X)[0]

    result = {
        col: str(prediction[i]) if i < len(prediction) else f"остальное{i+1}"
        for i, col in enumerate(LEVEL_COLS)
    }
    result["input"] = course_name
    return result
