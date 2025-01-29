import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from docx import Document
from PyPDF2 import PdfReader

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
    """
    response = model.generate_content(prompt)
    result = response.text
    return result

def extract_text_from_docx(file):
    document = Document(file)
    full_text = [paragraph.text for paragraph in document.paragraphs]
    return "\n".join(full_text)

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    full_text = [page.extract_text() for page in pdf_reader.pages]
    return "\n".join(full_text)

st.title("Note Summarizer with File Uploads")
st.write("Upload your notes (in .docx or .pdf format) and get a summarized version.")

uploaded_file = st.file_uploader("Upload a file (.docx, .pdf):", type=["docx", "pdf"])

if uploaded_file:
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        note_text = extract_text_from_docx(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        note_text = extract_text_from_pdf(uploaded_file)
    else:
        st.error("Unsupported file type.")
        note_text = None
else:
    note_text = st.text_area("Or enter your note here:", "")

if st.button("Summarize"):
    if note_text:
        summary = summarize_note(note_text)
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.warning("Please upload a file or enter text to summarize.")
