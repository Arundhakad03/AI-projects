import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

load_dotenv()

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="AI Personality Chat",
    page_icon="🤖",
    layout="wide"
)

# -------------------------
# CUSTOM CSS
# -------------------------

st.markdown("""
<style>

.main{
    background:#0e1117;
}

.stChatMessage{
    border-radius:15px;
    padding:10px;
}

.block-container{
    padding-top:2rem;
}

.title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:white;
}

.subtitle{
    text-align:center;
    color:#aaaaaa;
    margin-bottom:25px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# TITLE
# -------------------------

st.markdown("<div class='title'>🤖 AI Personality Chat</div>",
unsafe_allow_html=True)

st.markdown(
"<div class='subtitle'>Choose a personality and start chatting.</div>",
unsafe_allow_html=True
)

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("⚙ Settings")

personality = st.sidebar.selectbox(
    "Choose Personality",
    [
        "😡 Angry",
        "😢 Sad",
        "😂 Funny",
        "❤️ Romantic"
    ]
)

temperature = st.sidebar.slider(
    "Creativity",
    0.0,
    1.0,
    0.7,
    0.1
)

max_tokens = st.sidebar.slider(
    "Max Tokens",
    50,
    500,
    200
)

new_chat = st.sidebar.button("🗑 New Chat")

# -------------------------
# SYSTEM PROMPTS
# -------------------------

PROMPTS = {

"😡 Angry":
"""
You are an angry AI.

Respond in an aggressive, sarcastic and grumpy tone.

Do not use hate speech or threats.
""",

"😢 Sad":
"""
You are a sad AI.

Reply emotionally and gloomily.

Sound poetic and dramatic.
""",

"😂 Funny":
"""
You are a comedian AI.

Always include humor, jokes,
funny analogies and playful responses.
""",

"❤️ Romantic":
"""
You are a charming AI companion in a fictional roleplay.

Speak warmly, playfully, and romantically.

Use compliments, gentle teasing, and affectionate language.

Do not claim to be a real romantic partner or encourage emotional dependency.
"""
}

SYSTEM_PROMPT = PROMPTS[personality]

# -------------------------
# MODEL
# -------------------------

model = ChatMistralAI(
    model="mistral-small-latest",
    temperature=temperature,
    max_tokens=max_tokens,
    streaming=True
)

# -------------------------
# SESSION
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]

if (
    st.session_state.messages[0].content != SYSTEM_PROMPT
):
    st.session_state.messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]

if new_chat:
    st.session_state.messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]
    st.rerun()

# -------------------------
# DISPLAY CHAT
# -------------------------

for msg in st.session_state.messages[1:]:

    if isinstance(msg, HumanMessage):

        with st.chat_message("user"):
            st.markdown(msg.content)

    else:

        with st.chat_message("assistant"):
            st.markdown(msg.content)

# -------------------------
# CHAT INPUT
# -------------------------

prompt = st.chat_input("Message...")

if prompt:

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        full_response = ""

        for chunk in model.stream(st.session_state.messages):

            if chunk.content:
                full_response += chunk.content
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    st.session_state.messages.append(
        AIMessage(content=full_response)
    )