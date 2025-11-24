import requests
from config import BACKEND_URL


def _get(path: str):
    try:
        r = requests.get(f"{BACKEND_URL}{path}", timeout=10)
        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code}", "path": path}
        return r.json()
    except Exception as e:
        return {"error": str(e), "path": path}


def _post(path: str):
    try:
        r = requests.post(f"{BACKEND_URL}{path}", timeout=10)
        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code}", "path": path}
        return r.json()
    except Exception as e:
        return {"error": str(e), "path": path}


def get_student_record(student_id: str):
    if not student_id:
        return {"error": "student_id missing"}
    return _get(f"/student/{student_id}")


def get_completed_exams(student_id: str):
    if not student_id:
        return {"error": "student_id missing"}
    return _get(f"/student/{student_id}/completed")


def get_available_exams(student_id: str):
    if not student_id:
        return {"error": "student_id missing"}
    return _get(f"/student/{student_id}/available")


def get_enrolled_courses(student_id: str):
    if not student_id:
        return {"error": "student_id missing"}
    return _get(f"/student/{student_id}/courses")


def get_gpa(student_id: str):
    if not student_id:
        return {"error": "student_id missing"}
    return _get(f"/student/{student_id}/gpa")


def book_exam(student_id: str, exam_id: str):
    if not student_id or not exam_id:
        return {"error": "student_id and exam_id required"}
    return _post(f"/student/{student_id}/book/{exam_id}")


def get_booked_exams(student_id: str):
    if not student_id:
        return {"error": "student_id missing"}
    return _get(f"/student/{student_id}/bookings")


def get_next_exams(student_id: str):
    if not student_id:
        return {"error": "student_id missing"}
    return _get(f"/student/{student_id}/next_exams")
