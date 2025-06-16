from fastapi import FastAPI, UploadFile, HTTPException
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

@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile):
    try:
        # Ensure the uploaded file is a PDF
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

        # Read the uploaded PDF file
        pdf_file = await file.read()

        # Open the PDF file using PyMuPDF
        try:
            pdf_document = fitz.open(stream=pdf_file, filetype="pdf")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to open PDF file: {str(e)}")

        # Extract text from each page
        text = ""
        for page in pdf_document:
            try:
                text += page.get_text()
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to extract text from page: {str(e)}")

        # Analyze extracted text and predict job roles
        predicted_jobs = set()
        for keyword, job in keywords_to_jobs.items():
            if keyword.lower() in text.lower():
                predicted_jobs.add(job)

        return {
            "extracted_text": text,
            "predicted_jobs": list(predicted_jobs) if predicted_jobs else ["No relevant job roles found"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the resume: {str(e)}")