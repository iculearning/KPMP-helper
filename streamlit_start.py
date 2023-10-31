from backend.core import run_llm
import streamlit as st
from streamlit_chat import message
import subprocess


st.header("KPMP Documentation Helper")
st.subheader("2023 Sami Safadi, MD")
prompt = st.text_input("Enter your query below", "")

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

if prompt:
    with st.spinner("generating response..."):
        answer = run_llm(prompt)
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(answer)

if st.session_state["chat_answers_history"] and st.session_state["user_prompt_history"]:
    for question, answer in zip(
        reversed(st.session_state["user_prompt_history"]),
        reversed(st.session_state["chat_answers_history"]),
    ):
        message(question, avatar_style="personas", is_user=True)
        message(answer)
