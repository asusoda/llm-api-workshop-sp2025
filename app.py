import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

load_dotenv()

API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def summarize_note(note_text):
    prompt = f"""
    You are a helpful assistant. Your task is to summarize the following note in a clear, concise, and easy-to-understand format.
    Please summarize the key points while preserving the important information. Avoid unnecessary details.

    Note:
    {note_text}

    Summary:
    """

    response = model.generate_content(prompt)

    result = response.text
    
    return result
    
st.title("Note Summarizer")
st.write("Enter your notes and get a summarized version of it.")

note_text = st.text_area("Enter your note here:", "")

if st.button("Summarize"):
    if note_text:
        summary = summarize_note(note_text)
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.warning("Please enter a note to summarize.")
