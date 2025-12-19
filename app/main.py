from fastapi import FastAPI
from app.chat import app as chat_app
from app.internal.router import router as internal_router

app = FastAPI()

app.mount("/chat", chat_app)
app.include_router(internal_router, prefix="/internal")
