# College Essay Analyzer

This project provides AI-powered feedback on college essays using a fine-tuned GPT-2 model. Users can submit essays as text or upload files (PDF/DOCX), and receive instant, actionable feedback.

**Live Model:**  
Access the fine-tuned GPT-2 model here:  
https://huggingface.co/sudhanbhandari0/Essay_College_test

---

## Features

- Analyze essays and receive AI-generated feedback
- Upload essays as PDF or DOCX files
- Google authentication for secure login
- Essay and file storage with AWS S3
- Modern React frontend

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Python, AWS S3, Hugging Face Transformers
- **Frontend:** React.js

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js & npm
- AWS account (for S3)
- Google OAuth credentials

### Backend Setup

1. Install dependencies:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```
2. Set up environment variables in a `.env` file:
    ```
    AWS_ACCESS_KEY_ID=your_aws_key
    AWS_SECRET_ACCESS_KEY=your_aws_secret
    AWS_REGION=your_aws_region
    GOOGLE_CLIENT_ID=your_google_client_id
    ```
3. Run the backend server:
    ```bash
    uvicorn main:app --reload
    ```

### Frontend Setup

1. Install dependencies:
    ```bash
    cd frontend
    npm install
    ```
2. Start the React app:
    ```bash
    npm start
    ```

---

## API Endpoints

- `POST /api/analyze-essay` — Analyze essay text and get feedback
- `POST /api/upload-essay-file` — Upload essay file (PDF/DOCX) for analysis
- `POST /api/auth/google` — Google OAuth authentication

---
