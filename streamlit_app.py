from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

description = """
This programs allows the user to ask questions regarding the Kidney Precision Medicine Project (KPMP) using a natural language interface. 

It uses a large language model (ChatGPT) supplemented by the study protocol via a retrieval-augmented generation (RAG) method to generate the answers.

At this point, the October 2023 versions of the clinical protocol, and recruitment site MOP are available to search. 

&#169; 2023 Sami Safadi, MD. Email me at samisaf@gmail.com for questions.
"""
st.header("KPMP Documentation Helper")
st.markdown(description)
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
