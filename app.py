# app.py
import streamlit as st
from chat_app import run_agent

st.set_page_config(page_title="Resume Chat", page_icon="💬")
st.title("🧠 Resume Assistant Chat")

# Chat history state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
query = st.chat_input("Search resumes (e.g., accounting, budgeting)...")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("🔎 Searching and summarizing resumes..."):
        # Generate LLM response
        response = run_agent(query)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)