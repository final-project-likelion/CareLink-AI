from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os, json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter(prefix="/article-summary")

class ArticleSummaryRequest(BaseModel):
    title: str
    content: str

article_summary_system_prompt = """
You are an assistant that generates a correct and concise summary
of a Korean news article for cognitive training purposes.

Rules:
- Base the summary strictly on the article content.
- Do not add opinions, interpretations, or new information.
- Do not invent facts.
- Use clear and easy-to-understand Korean sentences.
- Limit the summary to 1 or 2 sentences.
- This summary will be used as the reference answer for cognitive training.

Output format (JSON only):
{
  "summary": "..."
}
"""

@router.post("")
def generate_article_summary(request: ArticleSummaryRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": article_summary_system_prompt},
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
    return json.loads(raw)
