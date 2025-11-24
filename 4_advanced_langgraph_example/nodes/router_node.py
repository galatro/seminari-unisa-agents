from state import AppState
from config import llm

class RouterNode:
    PROMPT = """
Sei un classificatore.

Classifica la domanda in una di queste categorie:

- STUDENTE → record personale, esami sostenuti, GPA, prenotazioni
- CAMPUS → aule, orari, professori, calendario esami dei corsi
- UNKNOWN → domanda fuori dominio universitario

Rispondi SOLO con:
STUDENTE, CAMPUS oppure UNKNOWN

Domanda:
\"\"\"{query}\"\"\"
"""

    def __call__(self, state: AppState) -> AppState:
        query = state.input_text

        result = llm.invoke(self.PROMPT.format(query=query)).content.strip().upper()

        if "STUDENT" in result or "STUDENTE" in result:
            state.domain = "student"
        elif "CAMPUS" in result:
            state.domain = "campus"
        else:
            state.domain = "unknown"

        return state
