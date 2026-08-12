import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

st.set_page_config(page_title="Haru 💌", page_icon="💗", layout="centered")

# ---------- Romantic Theme CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&family=Quicksand:wght@400;500;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #ffe4ec 0%, #ffd6e8 40%, #ffc2dd 100%);
}

html, body, [class*="css"]  {
    font-family: 'Quicksand', sans-serif;
}

#haru-title {
    font-family: 'Dancing Script', cursive;
    font-size: 3.2rem;
    text-align: center;
    color: #d1477a;
    margin-bottom: 0;
    text-shadow: 1px 1px 6px rgba(209, 71, 122, 0.25);
}

#haru-subtitle {
    text-align: center;
    color: #a85374;
    font-size: 1.05rem;
    margin-top: 0;
    margin-bottom: 1.5rem;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 20px;
    padding: 0.4rem 0.9rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 2px 10px rgba(209, 71, 122, 0.12);
}

div[data-testid="stChatMessageContent"] p {
    color: #6b2c46;
}

/* User messages */
[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    background-color: #fff0f5;
}

/* Assistant messages */
[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
    background: linear-gradient(135deg, #ffb6c1 0%, #ff9ebb 100%);
}

/* Chat input box */
[data-testid="stChatInput"] {
    border-radius: 25px;
    border: 2px solid #f6a6c1 !important;
}

/* Hearts divider */
.hearts-divider {
    text-align: center;
    color: #e485a6;
    letter-spacing: 12px;
    margin: 0.5rem 0 1.2rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<p id='haru-title'>Haru 💗</p>", unsafe_allow_html=True)
st.markdown("<p id='haru-subtitle'>a little corner just for you two ✨</p>", unsafe_allow_html=True)
st.markdown("<div class='hearts-divider'>♡ ♡ ♡</div>", unsafe_allow_html=True)

# ---------- Model + chat state (same logic as original script) ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="you are a lovely AI agent and your name is Haru")
    ]

@st.cache_resource
def get_model():
    return ChatMistralAI(
        model="mistral-small-latest",
        temperature=0,
        max_tokens=100
    )

model = get_model()

# Render existing conversation
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="💗"):
            st.markdown(msg.content)

# Chat input
prompt = st.chat_input("Say something to Haru...")

if prompt:
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    response = model.invoke(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=response.content))

    with st.chat_message("assistant", avatar="💗"):
        st.markdown(response.content)