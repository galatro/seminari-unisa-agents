from fastapi import APIRouter
from app.data import load_json, save_json

router = APIRouter()

@router.get("/all")
def get_student_record():
    students = load_json("students.json")
    return students

@router.get("/{student_id}")
def get_student_record(student_id: str):
    students = load_json("students.json")
    return students.get(student_id, None)

@router.get("/{student_id}/completed")
def get_completed_exams(student_id: str):
    exams = load_json("completed_exams.json")
    return exams.get(student_id, [])

@router.get("/{student_id}/available")
def get_available_exams(student_id: str):
    available = load_json("available_exams.json")
    return available.get(student_id, [])

@router.get("/{student_id}/courses")
def get_enrolled_courses(student_id: str):
    data = load_json("students.json")
    return data.get(student_id, {}).get("courses", [])

@router.get("/{student_id}/gpa")
def get_gpa(student_id: str):
    completed = load_json("completed_exams.json").get(student_id, [])
    if not completed:
        return {"gpa": None}
    total = sum([e["grade"] * e["credits"] for e in completed])
    credits = sum([e["credits"] for e in completed])
    return {"gpa": round(total/credits, 2)}

@router.post("/{student_id}/book/{exam_id}")
def book_exam(student_id: str, exam_id: str):
    # --- VALID STUDENT ---
    students = load_json("students.json")
    if student_id not in students:
        return {"error": "Student not found"}

    # --- LOAD DATA ---
    available_exams = load_json("available_exams.json").get(student_id, [])
    bookings = load_json("bookings.json")

    # --- ENSURE STRUCTURE ---
    # bookings.json must be a dict of lists
    if student_id not in bookings or not isinstance(bookings[student_id], list):
        bookings[student_id] = []

    # --- CHECK IF EXAM IS BOOKABLE ---
    valid_exam_ids = {exam["exam_id"] for exam in available_exams}
    if exam_id not in valid_exam_ids:
        return {
            "error": "Exam not available for this student",
            "exam_id": exam_id
        }

    # --- CHECK IF ALREADY BOOKED ---
    if exam_id in bookings[student_id]:
        return {
            "status": "already booked",
            "exam_id": exam_id
        }

    # --- PERFORM REAL BOOKING ---
    bookings[student_id].append(exam_id)
    save_json("bookings.json", bookings)

    return {
        "status": "booked",
        "student_id": student_id,
        "exam_id": exam_id
    }

@router.get("/{student_id}/bookings")
def get_booked_exams(student_id: str):
    students = load_json("students.json")
    if student_id not in students:
        return {"error": "student not found"}

    bookings = load_json("bookings.json")

    # Ensure structure
    booked = bookings.get(student_id, [])
    if not isinstance(booked, list):
        booked = []

    return {
        "student_id": student_id,
        "booked_exams": booked
    }


@router.get("/{student_id}/next_exams")
def get_next_exams(student_id: str):
    students = load_json("students.json")
    if student_id not in students:
        return {"error": "student not found"}

    courses = students[student_id]["courses"]
    exams = load_json("exams.json")
    completed = {e["course"] for e in load_json("completed_exams.json").get(student_id, [])}

    upcoming = []
    for course in courses:
        if course in exams:
            # take only exams for non-completed courses
            if course not in completed:
                upcoming.extend(exams[course])

    # sort by date
    upcoming = sorted(upcoming, key=lambda x: x["date"])
    return {"upcoming_exams": upcoming}
