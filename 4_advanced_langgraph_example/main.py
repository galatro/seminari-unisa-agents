import uuid
import traceback
import time
import json
from datetime import datetime

from config import DEFAULT_STUDENT_ID, evaluator
from state import AppState
from graph_app import build_graph

from tabulate import tabulate


def pretty_print_evaluation(eval_result):
    print("\n" + "=" * 70)
    print("📊 AGENTIC EVALUATION RESULTS".center(70))
    print("=" * 70 + "\n")

    def get_attr(obj, name, default=None):
        if isinstance(obj, dict):
            return obj.get(name, default)
        return getattr(obj, name, default)

    metrics = getattr(eval_result, "metrics_results", []) or []
    if metrics:
        rows = []
        explanations_to_print = []

        seen_global_metrics = set()

        for m in metrics:
            metric_name = get_attr(m, "name")
            node_name = get_attr(m, "node_name")

            if not node_name:
                if metric_name in seen_global_metrics:
                    continue
                seen_global_metrics.add(metric_name)

            rows.append([
                metric_name,
                get_attr(m, "group"),
                node_name,
                get_attr(m, "method"),
                get_attr(m, "provider"),
                get_attr(m, "value"),
            ])

            explanations = get_attr(get_attr(m, "additional_info"), 'explanations')
            if explanations:
                explanation_entry = get_attr(explanations[0], 'explanation')
                explanations_to_print.append({
                    "metric": get_attr(m, "name"),
                    "node": get_attr(m, "node_name"),
                    "explanation": explanation_entry
                })

        print("📌 Metriche per nodo:")
        print(
            tabulate(
                rows,
                headers=["Metrica", "Gruppo", "Nodo", "Metodo", "Provider", "Valore"],
                tablefmt="fancy_grid",
            )
        )
        print()

        if explanations_to_print:
            print("🔍 Dettagli metriche con spiegazioni:\n")
            for item in explanations_to_print:
                print(f"• Metrica: {item['metric']}  (Nodo: {item['node']})")
                print("  Spiegazione:")
                if isinstance(item["explanation"], dict):
                    print(json.dumps(item["explanation"], indent=4, ensure_ascii=False))
                else:
                    print(f"  {item['explanation']}")
                print()
    else:
        print("❗ Nessuna metrica singola registrata.\n")

    print("=" * 70 + "\n")


def run_agent(user_input: str, conversation_id: str, message_counter: int):
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

    evaluator.start_run()
    app = build_graph()
    final_state = app.invoke(state, config=config, debug=True)
    evaluator.end_run()

    answer = final_state.get("generated_text")
    domain = final_state.get("domain")
    tool_name = final_state.get("tool_name")
    tool_args = final_state.get("tool_args")
    tool_output = final_state.get("tool_output")

    eval_result = evaluator.get_result()

    return {
        "answer": answer,
        "domain": domain,
        "tool_name": tool_name,
        "tool_args": tool_args,
        "tool_output": tool_output,
        "interaction_id": interaction_id,
        "metrics": eval_result,
    }


def main():
    app = build_graph()
    conversation_id = str(uuid.uuid4())

    print("=== University Assistant (LangGraph + watsonx.ai + watsonx.governance) ===")
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
            evaluator.start_run()

            final_state = app.invoke(state, config=config)

            evaluator.end_run()

            answer = final_state.get("generated_text") or "(nessuna risposta generata)"
            domain = final_state.get("domain") or "sconosciuto"
            tool_name = final_state.get("tool_name")
            tool_args = final_state.get("tool_args") or {}

            print(f"\n📍 Dominio instradato: {domain}")
            print(f"🔖 Message ID: {interaction_id}")

            if tool_name:
                print(f"🛠️  Tool usato: {tool_name} {tool_args}")

            print(f"\n🤖 Assistente: {answer}\n")

            print("⏳ Recupero metriche...")
            time.sleep(1)

            try:
                eval_result = evaluator.get_result()
                pretty_print_evaluation(eval_result)
            except Exception as e:
                print(f"⚠️  Errore recupero metriche: {e}\n")

        except Exception as e:
            print(f"\n❌ Errore durante l'elaborazione:")
            print(f"   Message ID: {interaction_id}")
            print(f"\n{'=' * 60}")
            print("DETTAGLI ERRORE:")
            print('=' * 60)
            traceback.print_exc()
            print('=' * 60)
            print()

            try:
                evaluator.end_run()
            except:
                pass


if __name__ == "__main__":
    main()
