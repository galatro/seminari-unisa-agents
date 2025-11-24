import requests
from config import BACKEND_URL


def _get(path: str, params=None):
    try:
        r = requests.get(f"{BACKEND_URL}{path}", params=params, timeout=10)
        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code}", "path": path}
        return r.json()
    except Exception as e:
        return {"error": str(e), "path": path}



def get_class_schedule(course_code: str):
    """
    Restituisce la lista degli orari per un corso.
    """
    if not course_code:
        return {"error": "course_code missing"}
    return _get(f"/campus/schedule/{course_code}")


def get_room_availability(date: str, time_slot: str):
    """
    Restituisce le aule disponibili in un certo orario.
    """
    if not date or not time_slot:
        return {"error": "date and time_slot required"}

    return _get(
        "/campus/rooms/availability",
        params={"date": date, "time_slot": time_slot},
    )


def get_exam_calendar(course_code: str):
    """
    Restituisce il calendario degli esami per un corso.
    """
    if not course_code:
        return {"error": "course_code missing"}

    return _get(f"/campus/exams/{course_code}")


def get_professor_info(surname: str):
    """
    Restituisce tutte le informazioni di un professore.
    """
    if not surname:
        return {"error": "surname missing"}

    return _get(f"/campus/professor/{surname}")


def find_room_location(room_code: str):
    """
    Restituisce luogo, piano, edificio e descrizione di un’aula.
    """
    if not room_code:
        return {"error": "room_code missing"}

    return _get(f"/campus/room/{room_code}")


def get_all_courses():
    """
    Restituisce tutti i corsi disponibili.
    """
    return _get("/campus/courses")
