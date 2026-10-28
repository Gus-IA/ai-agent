import streamlit as st
from agent import run_agent

st.set_page_config(page_title="AI Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Agent")
st.caption("Ask anynthin - I can search the web, read files and tell you the time")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if question := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, steps = run_agent(question)

        st.markdown(answer)

        if steps:
            with st.expander(f"Tools used ({len(steps)})"):
                for step in steps:
                    st.markdown(f"**{step['tool']}**")
                    if step["args"]:
                        st.caption(f"Args: {step['args']}")
                    st.caption(f"Result: {step['result'][:150]}...")

        st.session_state.messages.append({"role": "assistant", "content": answer})
