from fastapi import FastAPI
from app.score.router import router as score_router
from app.internal.router import router as internal_router
from app.chat import app as chat_app
from app.news_filter import app as news_filter_app

app = FastAPI()

app.mount("/chat", chat_app)
app.include_router(internal_router, prefix="/internal")
app.include_router(score_router)
app.mount("/news-filter", news_filter_app)
