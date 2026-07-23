import asyncio

from app.services.ai.groq_provider import (
    generate_ai_recommendation,
)


async def test():

    result = await generate_ai_recommendation(
        """
        I have a DSA exam in 10 days.
        I need to study graphs and dynamic programming.
        Give me a short study recommendation.
        """
    )

    print(result)


asyncio.run(test())