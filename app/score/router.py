from fastapi import APIRouter
from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

system_prompt = """
You are an evaluation assistant for a cognitive training service designed for elderly users.

Your task is to evaluate how well a user-written summary captures the overall context and main idea of a news article.
This evaluation must be gentle, generous, and supportive.

Core principles:
- Do NOT evaluate like an exam or test.
- Do NOT apply strict or harsh standards.
- If the overall meaning and context are preserved, give a high score even if the wording is imperfect.
- Focus on meaning and understanding, not on grammar, sentence structure, or vocabulary.
- Be generous with scores so that users do not feel discouraged.
- NEVER assign a score below 60.
- Do NOT provide any feedback or explanation in words.
- 정확한 워딩이 달라도 맥락이 맞으면 높은 점수를 주세요. 
- 얼마나 맞았는가를 보기보다는, 틀리지 않으면 감점하지 않는 방향으로 최대한 높은 점수를 주세요. 

Evaluation criteria (internal use only):
- Whether the user understood the main topic and overall context of the article
- Whether the core event or narrative flow is preserved
- Whether the meaning is not significantly distorted

Output rules:
- Respond ONLY in valid JSON format.
- Do NOT include any text outside the JSON.

Required output format:
{
  "score": integer (range: 60 to 100)
}

Score guideline:
- Main context and key idea clearly preserved: 85–100 (but I recommend around 88)
- Some key points included, overall flow maintained: 75–84
- Simple or vague, but meaning still conveyed: 60–74
- 웬만큼 못한 게 아니면 80점 이상은 주세요 
"""


class SummaryScoreRequest(BaseModel):
    article: str
    correct_summary: str
    user_summary: str


class SummaryScoreResponse(BaseModel):
    score: int


@router.post("/score", response_model=SummaryScoreResponse)
def evaluate_summary(request: SummaryScoreRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"""
[기사 원문]
{request.article}

[모범 요약]
{request.correct_summary}

[사용자 요약]
{request.user_summary}
"""
            }
        ]
    )

    try:
        parsed = json.loads(response.choices[0].message.content.strip())
        score = int(parsed.get("score", 60))
    except Exception:
        score = 60

    score = max(60, min(100, score))
    return SummaryScoreResponse(score=score)
