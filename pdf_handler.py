# pdf_handler.py
import fitz  # PyMuPDF
import io

def extract_text_from_pdf(file_bytes):
    pdf_text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            pdf_text += page.get_text()
    return pdf_text
