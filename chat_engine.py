# chat_engine.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(question, context_text):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""
        You are an AI assistant. Answer the user's question based only on the PDF content below.
        ------------------
        PDF Content:
        {context_text[:8000]}  # Truncate if too long
        ------------------
        User's Question:
        {question}
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"
