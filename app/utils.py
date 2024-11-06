import PyPDF2
import pdfplumber
import docx
from io import BytesIO
from fastapi import HTTPException


async def extract_text_from_file_util(file_content: BytesIO, filename: str):
    file_type = filename.split('.')[-1].lower()

    try:
        if file_type == 'pdf':
            return await extract_text_from_pdf(file_content)
        elif file_type == 'docx':
            return await extract_text_from_docx(file_content)
        elif file_type == 'txt':
            return file_content.read().decode('utf-8')
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")


async def extract_text_from_pdf(file_content):
    try:
        with pdfplumber.open(file_content) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")



async def extract_text_from_docx(file_content):
    try:
        doc = docx.Document(file_content)
        text = ''
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")
