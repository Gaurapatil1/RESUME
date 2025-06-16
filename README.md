# Resume Analyzer Project

## Overview
The Resume Analyzer project allows users to upload their resumes in PDF format. The system extracts text from the uploaded document and predicts job roles based on predefined AI/ML-related keywords.

---

## Features Implemented Today
### Backend (`main.py`)
1. **FastAPI Setup**:
   - Created a FastAPI backend to handle resume uploads.
   - Enabled CORS for frontend-backend communication.

2. **PDF Text Extraction**:
   - Integrated PyMuPDF (`fitz`) to extract text from uploaded PDF files.
   - Added error handling for invalid file types and corrupted PDFs.

3. **Job Role Prediction**:
   - Defined a dictionary of AI/ML-related keywords mapped to job roles.
   - Implemented logic to analyze extracted text and predict job roles.

---

### Frontend (`index.html`)
1. **File Upload Interface**:
   - Designed a simple interface for users to upload resumes.
   - Added a button to trigger resume analysis.

2. **Display Results**:
   - Extracted text is displayed in a `<pre>` element.
   - Predicted job roles are listed in a `<ul>` element.

3. **JavaScript Logic**:
   - Used the Fetch API to send the uploaded file to the backend.
   - Handled errors gracefully and displayed appropriate messages.

---

### Jupyter Notebook
1. **PDF Text Extraction Testing**:
   - Tested PyMuPDF functionality in a Jupyter Notebook.
   - Verified text extraction from sample PDF files.

---

### Next Steps
1. Improve the job role prediction logic by integrating machine learning models.
2. Enhance the frontend design for better user experience.
3. Add support for additional file formats (e.g., `.docx`).
4. Write unit tests for backend functionality.

---

## How to Run
### Backend
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn fitz
