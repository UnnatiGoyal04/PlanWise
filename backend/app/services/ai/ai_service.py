from app.services.ai.mock_provider import (
    generate_task_reason,
)


async def explain_task_schedule(task):

    return await generate_task_reason(task)


async def generate_study_recommendation(tasks):

    high_priority = [
        task.title
        for task in tasks
        if task.priority == "High"
    ]

    if high_priority:
        summary = (
            "Focus on high priority tasks first "
            "to reduce deadline pressure."
        )
    else:
        summary = (
            "Maintain consistent progress across "
            "all subjects."
        )

    recommendations = [
        "Break large topics into smaller sessions.",
        "Revise difficult concepts regularly.",
    ]

    return {
        "summary": summary,
        "recommendations": recommendations,
    }