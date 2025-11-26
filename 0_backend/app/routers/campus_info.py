from fastapi import APIRouter
from app.data import load_json
from datetime import datetime

router = APIRouter()

@router.get("/schedule/{course_code}")
def get_class_schedule(course_code: str):
    schedule = load_json("schedule.json")   # lista
    return [s for s in schedule if s["course_id"].lower() == course_code.lower()]

def parse_slot(slot):
    start, end = slot.split("-")
    return (
        datetime.strptime(start, "%H:%M"),
        datetime.strptime(end, "%H:%M")
    )

@router.get("/rooms/availability")
def get_room_availability(date: str, time_slot: str):
    req_start, req_end = parse_slot(time_slot)

    rooms = load_json("rooms.json")
    available = []

    for r in rooms:
        dummy_slots = ["08:00-12:00", "14:00-18:00"]
        for slot in dummy_slots:
            slot_start, slot_end = parse_slot(slot)

            if req_start < slot_end and req_end > slot_start:
                available.append(r)
                break

    return available


@router.get("/exams/{course_code}")
def get_exam_calendar(course_code: str):
    exams = load_json("exams.json")
    return [e for e in exams if e["course_id"].lower() == course_code.lower()]

@router.get("/professor/{surname}")
def get_professor_info(surname: str):
    profs = load_json("professors.json")  # lista
    surname = surname.lower()

    for p in profs:
        if p["last_name"].lower() == surname:
            return p

    return "Non esiste un professore con quel cognome"

@router.get("/room/{room_code}")
def find_room_location(room_code: str):
    rooms = load_json("rooms.json")  # lista
    room_code = room_code.lower()

    for r in rooms:
        if r["room_id"].lower() == room_code:
            return {
                "room": r["room_id"],
                "building": r["building"],
                "floor": r.get("floor", "N/A"),
                "capacity": r["capacity"],
                "description": f"Piano {r.get('floor','?')} dell’edificio {r['building']}."
            }
    return "Non è stata trovata un'aula con questo codice"

@router.get("/courses")
def get_all_courses():
    courses = load_json("courses.json")
    return {"courses": courses}
