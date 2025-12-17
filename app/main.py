from fastapi import FastAPI
from app.chat import app as chat_app

app = FastAPI()

app.mount("/chat", chat_app)

