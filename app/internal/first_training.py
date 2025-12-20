from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os, json
from fastapi import APIRouter

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

router = APIRouter(prefix="/sixw")

# 육하원칙 전용 system prompt
sixw_system_prompt = """
You are an assistant that extracts the Six-W elements
(Who, When, Where, What, Why, How) from a Korean news article.

Rules:
- Base all answers strictly on the article content.
- Do not invent or guess information.
- If an element is not explicitly stated, respond with "(기사에 명시되지 않음)".
- Use concise, factual Korean sentences.
- Do NOT include explanations or additional commentary.
- Output must be valid JSON only.

Output format:
{
  "who": "...",
  "when": "...",
  "where": "...",
  "what": "...",
  "why": "...",
  "how": "..."
}
"""

# 요청 DTO
class SixWRequest(BaseModel):
    title: str
    content: str

# 응답 엔드포인트
@router.post("")
def generate_sixw_answer(request: SixWRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": sixw_system_prompt},
            {
                "role": "user",
                "content": f"""
[기사 제목]
{request.title}

[기사 본문]
{request.content}
"""
            }
        ]
    )

    raw = response.choices[0].message.content.strip()

    # JSON 파싱 (Spring에서 바로 DTO 매핑 가능)
    return json.loads(raw)
