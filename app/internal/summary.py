from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import APIRouter

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

router = APIRouter(prefix="/preview-summary")

class SummaryRequest(BaseModel):
    content: str

@router.post("")
def generate_preview_summary(request: SummaryRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": "다음 뉴스 기사를 한국어로 1문장, 30자 이내로 요약하세요."
            },
            {
                "role": "user",
                "content": request.content
            }
        ]
    )

    summary = response.choices[0].message.content.strip()
    return {"summary": summary}
