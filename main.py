# main.py
from pydantic import BaseModel

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

from fastapi import FastAPI, UploadFile, File
from pdf_handler import extract_text_from_pdf
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

# ✅ Mount static and templates folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

from chat_engine import ask_gemini

# Store the last extracted PDF text in memory (simplified for now)
pdf_context = {"text": ""}

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text_from_pdf(contents)
    pdf_context["text"] = text
    return {"message": "PDF uploaded successfully!", "sample_text": text[:500]}

@app.post("/ask/")
def ask_question(payload: QuestionRequest):
    question = payload.question
    if not pdf_context["text"]:
        return {"error": "Please upload a PDF first."}
    answer = ask_gemini(question, pdf_context["text"])
    return {"question": question, "answer": answer}

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
