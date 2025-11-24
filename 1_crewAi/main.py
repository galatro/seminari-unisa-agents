from crewai import Crew, Task
from agents.master_agent import master_agent
from agents.campus_agent import campus_agent
from agents.student_agent import student_agent
from config import STUDENT_ID
import json
import re

def classify(user_query: str) -> str:
    """
    Usa il Master Agent per determinare se la richiesta riguarda CAMPUS o STUDENTE.
    """
    task = Task(
        description=(
            "Classifica la seguente richiesta dell'utente come 'CAMPUS' o 'STUDENTE'. "
            "Rispondi SOLO con una di queste due parole.\n"
            f"Richiesta: {user_query}"
        ),
        expected_output="CAMPUS oppure STUDENTE.",
        agent=master_agent,
    )

    crew = Crew(agents=[master_agent], tasks=[task], verbose=False)
    result = str(crew.kickoff()).strip().upper()
    return "STUDENTE" if "STUDENTE" in result else "CAMPUS"


def extract_tools_used(output: str):
    """
    Estrae i tool chiamati dall'output CrewAI.
    """
    pattern = r"Tool\s+Used:\s*(.*?)\s*(?:\n|$)"
    return re.findall(pattern, output)


def run_agent(agent, user_query: str, domain: str):
    task = Task(
        description=(
            f"Rispondi in italiano alla richiesta dello studente.\n"
            f"Usa SOLO i tool disponibili per l'agente {domain}.\n\n"
            f"Richiesta: {user_query}"
        ),
        expected_output="Risposta chiara, veritiera e concisa.",
        agent=agent,
    )

    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = str(crew.kickoff())

    # Estrai i tool usati
    tools = extract_tools_used(result)

    print("\n🛠️  TOOL UTILIZZATI:")
    if tools:
        for t in tools:
            print(f"   - {t}")
    else:
        print("   (Nessun tool rilevato)")

    return result


def main():
    print("=== University Assistant — CrewAI + Watsonx ===")
    print("Scrivi una domanda (es. 'Che esami posso prenotare?').")
    print("Digita 'esci' per terminare.\n")

    while True:
        user_query = input("🧑 Tu: ").strip()
        if user_query.lower() in ["esci", "exit", "quit"]:
            print("👋 A presto!")
            break

        # Step 1 → routing
        domain = classify(user_query)
        print(f"\n🔎 Dominio rilevato → {domain}")

        # Step 2 → esegui l'agente giusto
        if domain == "CAMPUS":
            answer = run_agent(campus_agent, user_query, "CampusInfoAgent")
        else:
            answer = run_agent(student_agent, user_query, "StudentRecordAgent")

        print(f"\n🤖 Assistant: {answer}\n")


if __name__ == "__main__":
    main()
