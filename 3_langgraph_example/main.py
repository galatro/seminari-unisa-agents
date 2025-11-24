# main.py
import uuid
import traceback
from datetime import datetime

from config import DEFAULT_STUDENT_ID
from state import AppState
from graph_app import build_graph


def run_agent(user_input: str, conversation_id: str, message_counter: int):
    """
    Runs the LangGraph agent + watsonx.governance evaluation
    Returns:
        dict containing:
         - answer
         - domain
         - tool_name
         - tool_args
         - tool_output
         - interaction_id
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    interaction_id = f"msg_{conversation_id[:8]}_{message_counter:03d}_{timestamp}"

    # Build state
    state = AppState(
        input_text=user_input,
        student_id=DEFAULT_STUDENT_ID,
        interaction_id=interaction_id,
    )

    config = {
        "configurable": {
            "interaction_id": interaction_id,
            "conversation_id": conversation_id,
            "user_id": DEFAULT_STUDENT_ID,
            "timestamp": timestamp,
        }
    }

    # Run agent
    app = build_graph()
    final_state = app.invoke(state, config=config)

    answer = final_state.get("generated_text")
    domain = final_state.get("domain")
    tool_name = final_state.get("tool_name")
    tool_args = final_state.get("tool_args")
    tool_output = final_state.get("tool_output")


    return {
        "answer": answer,
        "domain": domain,
        "tool_name": tool_name,
        "tool_args": tool_args,
        "tool_output": tool_output,
        "interaction_id": interaction_id,
    }

def main():
    app = build_graph()
    conversation_id = str(uuid.uuid4())

    print("=== University Assistant (LangGraph + watsonx.ai) ===")
    print(f"Conversation ID: {conversation_id}")
    print("Scrivi una domanda. Digita 'exit' per uscire.\n")

    message_counter = 0

    while True:
        user_input = input("🧑 Tu: ").strip()

        if user_input.lower() in {"exit", "quit", "esci"}:
            print("👋 Ciao!")
            break

        message_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        interaction_id = f"msg_{conversation_id[:8]}_{message_counter:03d}_{timestamp}"

        state = AppState(
            input_text=user_input,
            student_id=DEFAULT_STUDENT_ID,
            interaction_id=interaction_id,
        )

        config = {
            "configurable": {
                "interaction_id": interaction_id,
                "conversation_id": conversation_id,
                "user_id": DEFAULT_STUDENT_ID,
                "timestamp": timestamp,
            }
        }

        try:
            final_state = app.invoke(state, config=config)
            answer = final_state.get("generated_text") or "(nessuna risposta generata)"
            domain = final_state.get("domain") or "sconosciuto"
            tool_name = final_state.get("tool_name")
            tool_args = final_state.get("tool_args") or {}

            print(f"\n📍 Dominio instradato: {domain}")
            print(f"🔖 Message ID: {interaction_id}")

            if tool_name:
                print(f"🛠️  Tool usato: {tool_name} {tool_args}")

            print(f"\n🤖 Assistente: {answer}\n")


        except Exception as e:
            print(f"\n❌ Errore durante l'elaborazione:")
            print(f"   Message ID: {interaction_id}")
            print(f"\n{'=' * 60}")
            print("DETTAGLI ERRORE:")
            print('=' * 60)
            traceback.print_exc()
            print('=' * 60)
            print()



if __name__ == "__main__":
    main()
