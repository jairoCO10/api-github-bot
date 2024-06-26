from fastapi import FastAPI, Request
import requests
from dotenv import load_dotenv
import uvicorn
import os


load_dotenv()

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID =os.getenv("TELEGRAM_CHAT_ID")   # ID del chat o grupo donde quieres enviar las notificaciones
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def send_telegram_message(message):
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(TELEGRAM_API_URL, json=payload)
    return response.json()

@app.post("/github-webhook")
async def github_webhook(request: Request):
    data = await request.json()
    commits = data.get('commits', [])
    repository = data['repository']['full_name']
    pusher = data['pusher']['name']

    for commit in commits:
        message = f"📌 <b>{repository}</b>\n📝 <b>{pusher}</b> hizo un commit:\n\n{commit['message']}\n🔗 <a href='{commit['url']}'>Ver Commit</a>"
        send_telegram_message(message)

    return {"status": "ok"}

if __name__ == '__main__':
    
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)

