from fastapi import FastAPI, UploadFile, HTTPException
import fitz  # PyMuPDF

app = FastAPI()

@app.post("/extract-pdf")
async def extract_pdf(file: UploadFile):
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

        return {"content": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the PDF: {str(e)}")