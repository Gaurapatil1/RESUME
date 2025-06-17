from fastapi import FastAPI, UploadFile, HTTPException, Form
from typing import List
import fitz  # PyMuPDF
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Predefined AI/ML-related keywords and job suggestions
keywords_to_jobs = {
    "TensorFlow": "AI Researcher",
    "Pytorch": "AI Researcher",
    "Machine Learning": "Data Scientist",
    "Deep Learning": "Data Scientist",
    "NLP": "AI Researcher",
    "Python": "Software Engineer",
    "SQL": "Data Analyst",
    "Cybersecurity": "Cybersecurity Analyst",
}

@app.post("/analyze-resumes")
async def analyze_resumes(files: List[UploadFile]):
    results = []
    for file in files:
        try:
            # Ensure the uploaded file is a PDF
            if file.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail=f"Invalid file type for {file.filename}. Please upload a PDF file.")

            # Read the uploaded PDF file
            pdf_file = await file.read()

            # Open the PDF file using PyMuPDF
            try:
                pdf_document = fitz.open(stream=pdf_file, filetype="pdf")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to open PDF file {file.filename}: {str(e)}")

            # Extract text from each page
            text = ""
            for page in pdf_document:
                try:
                    text += page.get_text()
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Failed to extract text from page in {file.filename}: {str(e)}")

            # Analyze extracted text and predict job roles
            predicted_jobs = set()
            ats_score = 0
            for keyword, job in keywords_to_jobs.items():
                if keyword.lower() in text.lower():
                    predicted_jobs.add(job)
                    ats_score += 10  # Increment ATS score for each matched keyword

            results.append({
                "filename": file.filename,
                "extracted_text": text,
                "predicted_jobs": list(predicted_jobs) if predicted_jobs else ["No relevant job roles found"],
                "ats_score": ats_score,
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e),
            })

    return results