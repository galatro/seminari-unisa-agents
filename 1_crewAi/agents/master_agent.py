from crewai import Agent
from config import llm

master_agent = Agent(
    name="UniversityMasterAgent",
    role="Router richieste universitarie",
    goal="Decidere se una richiesta riguarda CAMPUS o STUDENTE.",
    backstory="Instradi correttamente tutte le richieste.",
    llm=llm
)
