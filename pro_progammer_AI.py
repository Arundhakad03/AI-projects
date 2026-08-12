import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(page_title="Groq Programmer Chat", page_icon="🤖")
st.title("🤖 Programmer Chat")
st.caption("Powered by Groq · Llama 3.3 70B")


def create_model():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        max_tokens=2000,
        temperature=0.3,
    )


if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content="You are a professional programmer. Keep replies concise and token-efficient."
        )
    ]

with st.sidebar:
    if st.button("Clear conversation"):
        st.session_state.messages = [
            SystemMessage(
                content="You are a professional programmer. Keep replies concise and token-efficient."
            )
        ]
        st.rerun()


for message in st.session_state.messages:
    if isinstance(message, SystemMessage):
        continue

    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)


if prompt := st.chat_input("Ask a programming question..."):
    if not os.getenv("GROQ_API_KEY"):
        st.error("Add GROQ_API_KEY to your .env file.")
        st.stop()

    st.session_state.messages.append(HumanMessage(content=prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        model = create_model()

        def reply_stream():
            for chunk in model.stream(st.session_state.messages):
                if chunk.content:
                    yield chunk.content

        reply = st.write_stream(reply_stream())
        st.session_state.messages.append(AIMessage(content=reply))