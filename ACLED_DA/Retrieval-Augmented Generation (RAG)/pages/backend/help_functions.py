import streamlit as st
import time

# Function to display typing effect
def display_typing_effect(text, delay=0.03):
    typed_text = ""
    placeholder = st.empty()  # Placeholder to update text incrementally
    for char in text:
        typed_text += char
        placeholder.markdown(typed_text)
        time.sleep(delay)  # Adjust typing speed here

