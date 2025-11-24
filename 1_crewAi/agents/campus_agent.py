from crewai import Agent
from config import llm
from tools.campus_tools import (
    get_class_schedule_tool,
    get_room_availability_tool,
    get_exam_calendar_tool,
    get_professor_info_tool,
    find_room_location_tool,
    get_all_courses_tool
)

campus_agent = Agent(
    name="CampusInfoAgent",
    role="Assistente logistica universitaria",
    goal="Fornire informazioni su corsi, aule, orari e professori.",
    backstory="Sei esperto della struttura del campus e dei calendari.",
    tools=[
        get_class_schedule_tool,
        get_room_availability_tool,
        get_exam_calendar_tool,
        get_professor_info_tool,
        find_room_location_tool,
        get_all_courses_tool
    ],
    llm=llm
)
