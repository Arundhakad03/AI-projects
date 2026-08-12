import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler


load_dotenv()


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert movie information extraction assistant.

Your task is to carefully read the paragraph provided by the user and extract all movie-related information mentioned in it.

Paragraph:

{paragraph}

Extract the following details, if they are mentioned or can be confidently inferred from the text:

- Movie Title
- Original Title (if mentioned)
- Release Date
- Release Year
- Runtime
- Genre(s)
- Language(s)
- Country of Origin
- Director(s)
- Writer(s)
- Producer(s)
- Music Composer
- Cinematographer
- Editor
- Production Company
- Distributor
- Main Cast (Actor → Character)
- Supporting Cast (if mentioned)
- Plot Summary (2–4 paragraphs or 100–150 words)
- Main Themes
- IMDb Rating (if mentioned)
- Rotten Tomatoes Rating (if mentioned)
- Metacritic Score (if mentioned)
- Budget (if mentioned)
- Worldwide Box Office Collection (if mentioned)
- Awards and Nominations (if mentioned)
- Interesting Facts or Trivia (if mentioned)
- Streaming Platforms (if mentioned)
- Short summary (mandatatory)

Formatting Instructions:
- Use clear section headings.
- Only extract information that is explicitly stated or can be confidently inferred from the paragraph.
- Do NOT invent or hallucinate missing information.
- If a detail is not available in the paragraph, write "Not Mentioned."
- Keep the extracted information concise, well-organized, and easy to read.
- Preserve the original meaning of the paragraph.
""",
        ),
        ("human", "extract the information from the paragraph.\n{paragraph}"),
    ]
)



paragraph = st.text_area("Enter paragraph", height=250)

def stream_response(model, final_prompt):
    for chunk in model.stream(final_prompt):
        if chunk.content:
            yield chunk.content

if st.button("Extract information"):
    if paragraph.strip():
        with st.spinner("Extracting movie information..."):
            model = ChatGroq(model="llama-3.3-70b-versatile")
            final_prompt = prompt.invoke({"paragraph": paragraph})

            st.write_stream(stream_response(model, final_prompt))
    else:
        st.warning("Please enter a paragraph.")
