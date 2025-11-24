import streamlit as st
import uuid
from main import run_agent, pretty_print_evaluation

import io
import sys

st.set_page_config(page_title="University Assistant", layout="wide")

st.title("🎓 University Assistant — LangGraph + watsonx.ai + watsonx.governance")

# Stato sessione
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "counter" not in st.session_state:
    st.session_state.counter = 0


# ================================
#   RENDER CHAT
# ================================
for msg in st.session_state.messages:

    # --- USER ---
    if msg["role"] == "user":
        st.chat_message("user").write(msg["text"])

    # --- ASSISTANT + METRICS ---
    else:
        st.chat_message("assistant").write(msg["text"])

        # mostriamo le metriche SOLO se ci sono
        if "metrics" in msg and msg["metrics"] is not None:
            with st.expander("📊 Metriche di governance"):
                
                # cattura l'output CLI della pretty printer
                buffer = io.StringIO()
                sys_stdout = sys.stdout
                sys.stdout = buffer
                pretty_print_evaluation(msg["metrics"])
                sys.stdout = sys_stdout

                st.code(buffer.getvalue(), language="")


# ================================
#   INPUT UTENTE
# ================================
user_message = st.chat_input("Scrivi un messaggio...")

if user_message:
    # 1. Aggiungi messaggio utente
    st.session_state.messages.append({
        "role": "user",
        "text": user_message
    })
    st.chat_message("user").write(user_message)

    # 2. Genera risposta
    st.session_state.counter += 1

    result = run_agent(
        user_input=user_message,
        conversation_id=st.session_state.conversation_id,
        message_counter=st.session_state.counter
    )

    answer = result["answer"]
    metrics = result["metrics"]

    # 3. Aggiungi messaggio assistant + METRICHE
    st.session_state.messages.append({
        "role": "assistant",
        "text": answer,
        "metrics": metrics
    })

    # 4. Render immediato (senza refresh)
    st.chat_message("assistant").write(answer)
    
    # pannello metriche anche live
    with st.expander("📊 Metriche di governance"):
        buffer = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buffer
        pretty_print_evaluation(metrics)
        sys.stdout = sys_stdout
        st.code(buffer.getvalue(), language="")
