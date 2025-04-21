# Multiple-pdf-Question-Answers


## 📋 Prerequisites

Before proceeding, make sure you have:

- Python 3.8 or higher installed  
- `pip` (Python Package Manager)

---

## ⚙️ Installation Steps

### 1. Set up a virtual environment (optional but recommended)
```bash
python -m venv venv
# Activate the virtual environment:
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 2. Install required libraries
```bash
pip install streamlit google-generativeai PyPDF2 fpdf
```

### 3. Obtain a Gemini AI API Key
- Go to [Google AI Studio](https://aistudio.google.com/)
- Sign in with your Google account
- Generate an API key

---

## 🔐 Configuring the API Key

Open the `app.py` file and replace the `API_KEY` variable with your actual Gemini API key:
```python
API_KEY = "your_actual_api_key_here"
```

---

## 🚀 Running the Application

```bash
streamlit run app.py
```

---

## ✨ Features

- Upload a PDF file  
- Extract text from the PDF  
- Ask questions about the content  
- View chat history  
- Download responses as a PDF  
- Upload a new PDF anytime  

---

## 🛠️ Troubleshooting

- **Streamlit not found?**  
  Run: `pip install streamlit`

- **API error?**  
  Ensure your API key is correct and your internet is working

- **PDF not extracting text?**  
  Make sure your PDF contains selectable text (not just scanned images)

