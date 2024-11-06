

from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from app.chromadb_client import ingest_document
from app.utils import extract_text_from_file_util
from io import BytesIO

router = APIRouter()


@router.post("/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    
    if not file.filename.endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    
    content = await file.read()

    
    background_tasks.add_task(process_file, content, file.filename)
    return {"message": "File is being processed in the background"}

async def process_file(content: bytes, filename: str):
    file_content = BytesIO(content)

    
    text = await extract_text_from_file_util(file_content, filename)

    
    await ingest_document(text, filename)



@router.post("/extract_text/")
async def extract_text_from_file(file: UploadFile = File(...)):
    try:
       
        content = await file.read()
        file_content = BytesIO(content)
        text = await extract_text_from_file_util(file_content, file.filename)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")
