import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
from fpdf import FPDF

# 🔑 Replace with your actual API key
API_KEY = "add your api key"

# Configure API key
genai.configure(api_key=API_KEY)

## ✅ Use a valid model name from your API list
MODEL_NAME = "models/gemini-2.0-flash"

# Initialize the model
model = genai.GenerativeModel(MODEL_NAME)

def extract_text_from_pdf(uploaded_file):
    """Extract complete text from uploaded PDF"""
    reader = PyPDF2.PdfReader(uploaded_file)
    text = "".join(page.extract_text() or "" for page in reader.pages)
    return text

st.title("📄 Chat with PDF using Gemini AI")

# ✅ Keep chat history even when changing PDFs
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ Upload PDF
if "upload_new_pdf" not in st.session_state:
    st.session_state.upload_new_pdf = False

if st.session_state.upload_new_pdf:
    uploaded_file = st.file_uploader("Upload a new PDF file", type=["pdf"], key="new_file_uploader")
else:
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"], key="file_uploader")

if uploaded_file:
    st.session_state.uploaded_file = uploaded_file  # Store the uploaded PDF
    st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)  # Extract text immediately
    st.session_state.upload_new_pdf = False  # Reset the flag after uploading

if "uploaded_file" in st.session_state and st.session_state.uploaded_file:
    st.text_area("Extracted Text (Full Document)", st.session_state.pdf_text, height=300)

    user_query = st.text_input("Ask a question about the document:")

    if st.button("Get Answer"):
        if user_query.strip():
            with st.spinner("Generating AI Response..."):
                prompt = f"Context: {st.session_state.pdf_text}\n\nQuestion: {user_query}\nAnswer:"
                response = model.generate_content(prompt)
                answer = response.text

                # ✅ Store chat history
                st.session_state.chat_history.append((user_query, answer))

                st.success("Response Generated!")
                st.write("**AI Response:**", answer)
        else:
            st.warning("Please enter a question!")

    # ✅ Display chat history (even if PDF changes)
    if st.session_state.chat_history:
        st.subheader("📜 Chat History")
        for i, (q, a) in enumerate(st.session_state.chat_history):
            st.write(f"**Q{i+1}:** {q}")
            st.write(f"**A{i+1}:** {a}")
            st.write("---")

    # ✅ Option to download responses as a PDF
    if st.button("Download Chat as PDF"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for i, (q, a) in enumerate(st.session_state.chat_history):
            pdf.multi_cell(0, 10, f"Q{i+1}: {q}")
            pdf.multi_cell(0, 10, f"A{i+1}: {a}")
            pdf.ln(5)

        pdf_content = pdf.output(dest="S").encode("latin1")  # ✅ Get string output
        pdf_buffer = io.BytesIO(pdf_content)  # ✅ Convert to BytesIO

        st.download_button(
            label="Download Chat History",
            data=pdf_buffer,
            file_name="chat_history.pdf",
            mime="application/pdf",
        )

    # ✅ Option to use the same PDF or upload a new one
    st.subheader("Choose an option:")
    choice = st.radio(
        "Do you want to continue with the current PDF or upload a new one?",
        ("Continue with current PDF", "Upload new PDF")
    )

    # ✅ When "Upload new PDF" is selected, reset only the PDF (not chat)
    if choice == "Upload new PDF":
        if st.button("Confirm New PDF Upload"):
            if "uploaded_file" in st.session_state:
                del st.session_state.uploaded_file
            if "pdf_text" in st.session_state:
                del st.session_state.pdf_text
            st.session_state.upload_new_pdf = True  # Set the flag to show the new file uploader
