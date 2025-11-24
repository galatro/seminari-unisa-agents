from crewai import Agent
from config import llm, STUDENT_ID
from tools.student_tools import (
    get_student_record_tool,
    get_completed_exams_tool,
    get_available_exams_tool,
    get_enrolled_courses_tool,
    get_student_gpa_tool,
    book_exam_tool,
    get_booked_exams_tool,
    get_next_exams_tool
)

student_agent = Agent(
    name="StudentRecordAgent",
    role="Assistente record studente",
    goal=f"Gestire le informazioni dello studente con id {STUDENT_ID}.",
    backstory="Conosci tutto il libretto e gli esami dello studente.",
    tools=[
        get_student_record_tool,
        get_completed_exams_tool,
        get_available_exams_tool,
        get_enrolled_courses_tool,
        get_student_gpa_tool,
        book_exam_tool,
        get_booked_exams_tool,
        get_next_exams_tool
    ],
    llm=llm
)
