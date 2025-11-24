import requests
from crewai.tools import tool
from config import BASE_URL, STUDENT_ID


@tool("get_student_record")
def get_student_record_tool(student_id: str = STUDENT_ID):
    """Restituisce il record completo dello studente (dati anagrafici e corsi)."""
    return requests.get(f"{BASE_URL}/student/{student_id}").text


@tool("get_completed_exams")
def get_completed_exams_tool(student_id: str = STUDENT_ID):
    """Restituisce gli esami completati dallo studente con voti e CFU."""
    return requests.get(f"{BASE_URL}/student/{student_id}/completed").text


@tool("get_available_exams")
def get_available_exams_tool(student_id: str = STUDENT_ID):
    """Restituisce l'elenco degli esami che lo studente può prenotare."""
    return requests.get(f"{BASE_URL}/student/{student_id}/available").text


@tool("get_enrolled_courses")
def get_enrolled_courses_tool(student_id: str = STUDENT_ID):
    """Restituisce la lista dei corsi in cui lo studente è attualmente iscritto."""
    return requests.get(f"{BASE_URL}/student/{student_id}/courses").text


@tool("get_student_gpa")
def get_student_gpa_tool(student_id: str = STUDENT_ID):
    """Restituisce la media ponderata (GPA) dello studente."""
    return requests.get(f"{BASE_URL}/student/{student_id}/gpa").text


@tool("book_exam")
def book_exam_tool(exam_id: str, student_id: str = STUDENT_ID):
    """Effettua la prenotazione di un esame per lo studente indicato."""
    return requests.post(
        f"{BASE_URL}/student/{student_id}/book/{exam_id}"
    ).text


@tool("get_booked_exams")
def get_booked_exams_tool(student_id: str = STUDENT_ID):
    """Restituisce tutti gli esami già prenotati dallo studente."""
    return requests.get(f"{BASE_URL}/student/{student_id}/bookings").text


@tool("get_next_exams")
def get_next_exams_tool(student_id: str = STUDENT_ID):
    """Restituisce i prossimi esami disponibili in calendario per lo studente."""
    return requests.get(f"{BASE_URL}/student/{student_id}/next_exams").text
