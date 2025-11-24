import streamlit as st
import uuid
from main import run_agent

import io
import sys

st.set_page_config(page_title="University Assistant", layout="wide")

st.title("🎓 University Assistant — LangGraph + watsonx.ai")

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

    else:
        st.chat_message("assistant").write(msg["text"])



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

    # 3. Aggiungi messaggio assistant
    st.session_state.messages.append({
        "role": "assistant",
        "text": answer,
    })

    # 4. Render immediato (senza refresh)
    st.chat_message("assistant").write(answer)
    
