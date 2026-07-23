from groq import Groq

from app.core.settings import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


async def generate_ai_recommendation(prompt: str) -> str:
    """
    Generates AI-based study recommendations using Groq LLM.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI study planner assistant. "
                    "Give practical and personalized study advice."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content