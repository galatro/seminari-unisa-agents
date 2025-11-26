from fastapi import APIRouter
from app.data import load_json, save_json

router = APIRouter()

def find_student(students, student_id):
    for s in students:
        if s["student_id"] == student_id:
            return s
    return None

@router.get("/all")
def get_student_record_all():
    return load_json("students.json")

@router.get("/{student_id}")
def get_student_record(student_id: str):
    students = load_json("students.json")
    return find_student(students, student_id)


@router.get("/{student_id}/completed")
def get_completed_exams(student_id: str):
    completed = load_json("completed_exams.json")

    return [
        e for e in completed
        if e["student_id"] == student_id
    ]


@router.get("/{student_id}/available")
def get_available_exams(student_id: str):
    available = load_json("available_exams.json")
    return [
        e for e in available
        if e["student_id"] == student_id
    ]


@router.get("/{student_id}/courses")
def get_enrolled_courses(student_id: str):
    students = load_json("students.json")
    s = find_student(students, student_id)
    if not s:
        return []
    return s["courses_enrolled"]


@router.get("/{student_id}/gpa")
def get_gpa(student_id: str):
    completed = [
        e for e in load_json("completed_exams.json")
        if e["student_id"] == student_id
    ]

    if not completed:
        return {"gpa": None}

    total = sum(e["grade"] * e["credits"] for e in completed)
    credits = sum(e["credits"] for e in completed)

    return {"gpa": round(total / credits, 2)}

@router.post("/{student_id}/book/{exam_id}")
def book_exam(student_id: str, exam_id: str):

    students = load_json("students.json")
    if not find_student(students, student_id):
        return {"error": "Student not found"}

    available = load_json("available_exams.json")
    av_for_student = [
        e for e in available if e["student_id"] == student_id
    ]

    valid_ids = {e["exam_id"] for e in av_for_student}
    if exam_id not in valid_ids:
        return {"error": "Exam not available"}

    # bookings is now a LIST
    bookings = load_json("bookings.json")

    # check duplicates
    for b in bookings:
        if b["student_id"] == student_id and b["exam_id"] == exam_id:
            return {"status": "already booked"}

    # perform booking
    bookings.append({
        "student_id": student_id,
        "exam_id": exam_id
    })

    save_json("bookings.json", bookings)

    return {"status": "booked", "exam_id": exam_id}


@router.get("/{student_id}/bookings")
def get_booked_exams(student_id: str):
    bookings = load_json("bookings.json")

    result = [
        b["exam_id"]
        for b in bookings
        if b["student_id"] == student_id
    ]

    return {"student_id": student_id, "booked_exams": result}


@router.get("/{student_id}/next_exams")
def get_next_exams(student_id: str):
    students = load_json("students.json")
    s = find_student(students, student_id)
    if not s:
        return {"error": "student not found"}

    student_courses = set(s["courses_enrolled"])

    completed = {
        e["course_id"]
        for e in load_json("completed_exams.json")
        if e["student_id"] == student_id
    }

    exams = load_json("exams.json")

    upcoming = [
        e for e in exams
        if e["course_id"] in student_courses and e["course_id"] not in completed
    ]
    upcoming = sorted(upcoming, key=lambda x: x["date"])
    return {"upcoming_exams": upcoming}
