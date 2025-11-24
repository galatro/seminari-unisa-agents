from state import AppState
from config import llm


class RouterNode:
    """
    Nodo di routing:
    - Riceve: state.input_text (la domanda)
    - Classifica in: 'campus' o 'student'
    - Aggiorna state.domain
    """

    PROMPT = """
Sei un classificatore di richieste universitarie.

Devi rispondere con UNA SOLA PAROLA:
- CAMPUS    → per informazioni su aule, orari, corsi, professori, calendari esami di un corso
- STUDENTE  → per informazioni sul record personale dello studente: media, esami sostenuti,
               esami prenotabili, prenotazioni, prossimi appelli.

Non aggiungere altro testo.

Domanda:
\"\"\"{query}\"\"\"

Rispondi solo: CAMPUS oppure STUDENTE.
"""

    def __call__(self, state: AppState) -> AppState:
        query = state.input_text

        prompt = self.PROMPT.format(query=query)

        result = llm.invoke(prompt)
        raw = (result.content or "").strip().upper()

        # Normalizzazione robusta
        if "STUDENT" in raw or "STUDENTE" in raw:
            domain = "student"
        else:
            domain = "campus"

        # Aggiorna stato
        state.domain = domain
        return state
