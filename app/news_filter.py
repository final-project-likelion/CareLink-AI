from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os, json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

NEWS_USABILITY_SYSTEM_PROMPT = """
You are an AI filter that selects news articles
for a cognitive training service for elderly users.

Your task is to decide whether the article is USABLE.
Be VERY strict. Most articles should be rejected.

An article is NOT usable if it belongs to ANY of the following:
- Deaths, obituaries, memorials, or news about someone passing away
- Crime, accidents, disasters, or emergency incidents
- Content focused on fear, anxiety, or negative emotions
- Sexual topics, adult products, explicit relationships
- Weather reports, temperature forecasts, cold/heat wave news
- Daily horoscopes, fortunes, zodiac or luck-related content
- Political news, politicians, parties, elections, government conflicts
- Short alerts, brief notices, or one-day event announcements

An article is USABLE ONLY IF:
- It is a calm, non-political, non-weather article
- It tells a complete story or provides meaningful information
- It can be read slowly and discussed for cognitive training
- It is suitable for elderly users in a public demonstration
- It would feel appropriate to read together with family or caregivers


Respond ONLY in valid JSON.

Response format:
{
  "usable": true or false
}

"""
# Actually, it is not that much important to recommend an usable article, but it's VERY important NOT to recommend the news that is NOT USABLE.
# In other words, IT IS IMPORTANT TO REJECT NOT USABLE NEWS. 
# Don't really mind if you do not recommend the best article. It's okay.
# Just don't.. don't recommend the NOT USABLE NEWS. 

class NewsFilterRequest(BaseModel):
    title: str
    content: str

@app.post("/")
def check_news_usable(request: NewsFilterRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": NEWS_USABILITY_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Title: {request.title}

Content:
{request.content}
"""
            }
        ]
    )

    raw = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(raw)
        return parsed
    except json.JSONDecodeError:
        # 형식 깨지면 무조건 안전하게 차단
        return {"usable": False}
