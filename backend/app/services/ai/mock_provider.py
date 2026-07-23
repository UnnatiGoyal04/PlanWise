async def generate_task_reason(task):
    """
    Generates an AI-style explanation
    for scheduling decisions.
    """

    reasons = []

    if task.priority == "High":
        reasons.append("high priority")

    if task.due_date:
        reasons.append("upcoming deadline")

    if task.estimated_hours:
        reasons.append(
            "requires significant preparation time"
        )

    if not reasons:
        reasons.append("overall study balance")

    return (
        "Scheduled because it has "
        + ", ".join(reasons)
        + "."
    )