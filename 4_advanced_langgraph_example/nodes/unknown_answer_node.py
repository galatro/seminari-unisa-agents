from state import AppState

def unknown_answer_node(state: AppState) -> dict:
    answer = """
Non riesco a rispondere alla domanda perché non riguarda il sistema universitario.

Puoi chiedermi informazioni su:
- esami sostenuti
- prenotazioni appelli
- orari delle aule
- corsi e professori
"""

    return {
        "generated_text": answer.strip(),
        "context": [],
        "tool_name": None,
        "tool_args": {},
        "tool_output": {},
        "tool_calls": [],
        "domain": "unknown",
    }
