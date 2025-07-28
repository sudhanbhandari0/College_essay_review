from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from database import get_db, Essay, FileModel
from ai_service import AIService
from file_utils import extract_text_from_pdf, extract_text_from_docx
from s3_utils import upload_file_to_s3
from google.oauth2 import id_token
from google.auth.transport import requests
from auth import create_access_token, get_current_user


import uuid
import tempfile
import os
import boto3
import re

app = FastAPI()
#load from .env filr
load_dotenv()
ai_service = AIService()

#boto3 is the AWS SDK for python
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# This defines the structure of essay data
class EssaySubmission(BaseModel):
    content: str
    author: str = "Anonymous"

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/api/analyze-essay")
def analyze_essay(essay: EssaySubmission, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    #print(f"User {current_user['sub']} is analyzing an essay")
    ai_feedback = ai_service.generate_feedback(essay.content)

    # Save essay to database
    db_essay = Essay(
        content=essay.content,
        author=current_user['sub'],
        content_length=len(essay.content),
        feedback=ai_feedback
    )
    db.add(db_essay)
    db.commit()
    db.refresh(db_essay)
    
    return {
        "message": "Essay saved successfully",
        "essay_id": db_essay.id,
        "content_length": len(essay.content),
        "author": essay.author,
        "feedback": ai_feedback
    }



#add File Upload Endpoint
# Creates a new endpoint that accepts file uploads
# Saves the file to S3
# Stores the file URL in the database
# Returns success message with file URL
@app.post("/api/upload-essay-file")
async def upload_essay_file(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    print(f"User {current_user['sub']} is uploading a file")
    """Upload essay file (PDF/DOC) to S3"""
    try:
        # Read file content
        file_content = await file.read()

        # 2. Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix="." + file.filename.split('.')[-1]) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name
        
        if file.filename.lower().endswith(".pdf"):
            essay_text = extract_text_from_pdf(tmp_path)
        elif file.filename.lower().endswith(".docx"):
            essay_text = extract_text_from_docx(tmp_path)
        else:
            essay_text = None

        essay_text = re.sub(r'\s+', ' ', essay_text).strip()
        # Generate a unique file name
        file_name = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        #with open(tmp_path, "rb") as f:
            #file_url = upload_file_to_s3(f.read(), file_name)

        # 5. Clean up temp file
        os.remove(tmp_path)

        if not essay_text:
            return {
                "message": "Could not extract text from file",
                "error": "Unsupported or empty file"
            }

        ai_feedback = ai_service.generate_feedback(essay_text)


        # Upload file to S3
        #print("Uploading file to S3 with name:", file_name)
        file_url = upload_file_to_s3(file_content, file_name)
        #print("S3 returned URL:", file_url)

        # 7. Save file info to database
        db_file = FileModel(
            url=file_url,
            filename=file.filename,
            content_type=file.content_type
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        # 8. Return response
        return {
            "message": "File uploaded and analyzed successfully",
            "file_url": file_url,
            "filename": file.filename,
            "file_id": db_file.id,
            "feedback": ai_feedback,
            "extracted_text": essay_text[:500]  # Preview for debugging
        }
    except Exception as e:
        return {
            "message": "Failed to upload or analyze file",
            "error": str(e)
        }

        
@app.on_event("startup")
async def startup_event():
    print("Loading AI model at startup...")
    ai_service.load_model()     

@app.post("/api/auth/google")
async def google_auth(payload: dict):
    token = payload.get("token")
    if not token:
        return {"error": "No token provided"}
    
    #verify token
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            os.getenv("GOOGLE_CLIENT_ID")
        )
        print("Verified token info:", idinfo)

        user_data = {
            "sub": idinfo["email"],
            "name": idinfo.get("name"),
            "email": idinfo["email"],
            "picture": idinfo.get("picture")
        }

        access_token = create_access_token(user_data)

        return {
            "jwt_token": access_token,
            "email": idinfo["email"],
            "name": idinfo.get("name"),
            "picture": idinfo.get("picture")
        }
    except ValueError:
        return {"error": "Invalid token"}