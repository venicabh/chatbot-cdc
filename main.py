@app.get("/")
def home():
    return {"message": "Chatbot do CDC está online!"}
    
from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    chat_id = data['message']['chat']['id']
    user_text = data['message']['text']
    
    resposta = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "messages": [{
                "role": "system",
                "content": "Você é um assistente jurídico do CDC. Responda citando artigos e súmulas."
            }, {
                "role": "user",
                "content": user_text
            }],
            "model": "mixtral-8x7b-32768"
        }
    ).json()['choices'][0]['message']['content']
    
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": resposta}
    )
    
    return {"status": "ok"}

# Endpoint para evitar suspensão no Render
@app.get("/health")
def health_check():
    return {"status": "active"}

# Adicione este endpoint ao seu main.py
@app.get('/keepalive')
def keepalive():
    return {"status": "keeping alive"}
