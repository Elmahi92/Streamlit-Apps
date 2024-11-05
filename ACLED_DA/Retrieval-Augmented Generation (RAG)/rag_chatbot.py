import streamlit as st
import time
from pages.backend import rag_functions
from pages.backend import help_functions

# ChatGPT-like theme
st.set_page_config(
    page_title="Chatbot - RAG",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# UNDP Logo
st.image("undp_logo.png", width=600)  # Assuming 'undp_logo.png' is in the same directory as the script

# Title and styling
st.markdown("""
    <style>
    .css-1y4p8pa { padding: 1rem 2rem; }  /* Top and side padding */
    .stButton>button { background-color: #1A73E8; color: white; border-radius: 12px; }
    .stChatMessage div[data-testid="stMarkdownContainer"] { padding: 0.6rem; border-radius: 8px; }
    .stChatMessage.stChatMessage--user { background-color: #E8F0FE; }
    .stChatMessage.stChatMessage--assistant { background-color: #F1F3F4; }
    </style>
    """, unsafe_allow_html=True)

title_text=st.title("Sudan Conflict Chatgpt: Your Updated Guide to Navigating the Crisis")

sub_title_text = (
    "This chatbot gives you the latest information on the Sudan conflict, "
    "using real-time updates from Situation Reports by OCHA. For more details, visit: "
    "[OCHA Sudan Situation Reports](https://reports.unocha.org/en/country/sudan/)"
)
st.write(sub_title_text)
#help_functions.display_typing_effect(sub_title_text)

token = ""
llm_model = "tiiuae/falcon-7b-instruct"
instruct_embeddings = "hkunlp/instructor-xl"
existing_vector_store = "Sudan"
temperature = 1.00
max_length = 300

# Prepare the LLM model
if "conversation" not in st.session_state:
    st.session_state.conversation = None

if token:
    st.session_state.conversation = rag_functions.prepare_rag_llm(
        token, llm_model, instruct_embeddings, existing_vector_store, temperature, max_length
    )

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Source documents
if "source" not in st.session_state:
    st.session_state.source = []

# Display chat history
for message in st.session_state.history:
    role = message["role"]
    with st.chat_message(role):
        st.markdown(message["content"])

# Function to display typing effect
def display_typing_effect(answer):
    typed_answer = ""
    for char in answer:
        typed_answer += char
        time.sleep(0.03)  # Adjust speed here (0.03 seconds between each character)
        st.markdown(typed_answer)
        st.experimental_rerun()

# User input for questions
if question := st.chat_input("Ask a question"):
    # Append user question to history
    st.session_state.history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Generate the assistant's answer
    answer, doc_source = rag_functions.generate_answer(question, token)
    
    # Simulate typing for the assistant's response
    with st.chat_message("assistant"):
        typed_response_placeholder = st.empty()  # Placeholder to update text incrementally
        typed_response = ""
        for char in answer:
            typed_response += char
            time.sleep(0.01)  # Typing speed
            typed_response_placeholder.markdown(typed_response)
    
    # Append assistant's final answer to history
    st.session_state.history.append({"role": "assistant", "content": answer})

    # Store the source of the document
    st.session_state.source.append({"question": question, "answer": answer, "document": doc_source})
