from fastapi import FastAPI
from app.chat import app as chat_app
from app.summary import app as summary_app

app = FastAPI()

app.mount("/chat", chat_app)
app.mount("/internal", summary_app)
