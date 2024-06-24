import os
import google.generativeai as genai
from decouple import config


genai.configure(api_key=config('GOOGLE_API_KEY'))


model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])
instruction = "In this chat, respond as if you're explaining things to a five-year-old child. "

def get_gemini_response(question):
    response = chat.send_message(instruction + question)
    result = response.text
    return result


print(get_gemini_response('what is python'))


