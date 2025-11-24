import requests
from crewai.tools import tool
from config import BASE_URL

@tool("get_class_schedule")
def get_class_schedule_tool(course_code: str):
    """Restituisce l'orario di un corso dato il course_code."""
    return requests.get(f"{BASE_URL}/campus/schedule/{course_code}").text


@tool("get_room_availability")
def get_room_availability_tool(date: str, time_slot: str):
    """Restituisce le aule disponibili in una data fascia oraria."""
    return requests.get(
        f"{BASE_URL}/campus/rooms/availability",
        params={"date": date, "time_slot": time_slot}
    ).text


@tool("get_exam_calendar")
def get_exam_calendar_tool(course_code: str):
    """Restituisce il calendario esami del corso."""
    return requests.get(
        f"{BASE_URL}/campus/exams/{course_code}"
    ).text


@tool("get_professor_info")
def get_professor_info_tool(surname: str):
    """Restituisce le informazioni del professore dato il cognome."""
    return requests.get(
        f"{BASE_URL}/campus/professor/{surname}"
    ).text


@tool("find_room_location")
def find_room_location_tool(room_code: str):
    """Restituisce la posizione dell'aula."""
    return requests.get(
        f"{BASE_URL}/campus/room/{room_code}"
    ).text


@tool("get_all_courses")
def get_all_courses_tool():
    """Restituisce la lista completa dei corsi."""
    return requests.get(f"{BASE_URL}/campus/courses").text
