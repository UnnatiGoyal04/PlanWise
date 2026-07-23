from app.services.ai.groq_provider import (
    generate_ai_recommendation,
)


async def explain_task_schedule(task):
    """
    Generates AI explanation for why a task
    was scheduled.
    """

    prompt = f"""
You are an AI study planner.

Explain why this task should be scheduled:

Task:
{task.title}

Subject:
{task.subject}

Priority:
{task.priority}

Due date:
{task.due_date}

Estimated hours:
{task.estimated_hours}

Give a short explanation in 1-2 sentences.
"""

    return await generate_ai_recommendation(
        prompt
    )


async def generate_study_recommendation(tasks):
    """
    Generates overall study recommendations.
    """

    task_information = "\n".join(
        [
            f"""
Title: {task.title}
Subject: {task.subject}
Priority: {task.priority}
Due date: {task.due_date}
Hours: {task.estimated_hours}
"""
            for task in tasks
        ]
    )

    prompt = f"""
You are an AI study planner.

Based on these tasks:

{task_information}

Give:
1. A short summary.
2. Three practical study recommendations.

Keep the response concise.
"""

    response = await generate_ai_recommendation(
        prompt
    )

    lines = [
        line.strip()
        for line in response.split("\n")
        if line.strip()
    ]  

    recommendations = [
        line.lstrip("0123456789.- ")
        for line in lines
        if line[0].isdigit()
    ]

    summary = response

    if "Practical Study Recommendations" in response:
        summary = response.split(
            "Practical Study Recommendations"
        )[0]
    summary = (
        summary
        .replace("**Summary**:", "")
        .replace("**", "")
        .strip()
    )

    return {
        "summary": summary.strip(),
        "recommendations": recommendations,
    }