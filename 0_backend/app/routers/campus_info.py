from fastapi import APIRouter
from app.data import load_json
from datetime import datetime

router = APIRouter()

@router.get("/schedule/{course_code}")
def get_class_schedule(course_code: str):
    schedule = load_json("schedule.json")
    return schedule.get(course_code, [])

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
        for slot in r["available_slots"]:
            slot_start, slot_end = parse_slot(slot)

            # Check overlap
            if req_start < slot_end and req_end > slot_start:
                available.append(r)
                break

    return available


@router.get("/exams/{course_code}")
def get_exam_calendar(course_code: str):
    exams = load_json("exams.json")
    return exams.get(course_code, [])

@router.get("/professor/{surname}")
def get_professor_info(surname: str):
    profs = load_json("professors.json")
    return profs.get(surname.lower(), None)

@router.get("/room/{room_code}")
def find_room_location(room_code: str):
    rooms = load_json("rooms.json")
    for r in rooms:
        if r["code"].lower() == room_code.lower():
            return {
                "room": r["code"],
                "building": r["building"],
                "floor": r["floor"],
                "capacity": r["capacity"],
                "description": f"Piano {r['floor']} dell’edificio {r['building']}."
            }
    return None

@router.get("/courses")
def get_all_courses():
    courses = load_json("courses.json")
    return {"courses": courses}
