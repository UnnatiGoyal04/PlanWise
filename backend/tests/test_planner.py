import pytest


@pytest.mark.asyncio
async def test_generate_plan_returns_tasks(
    client,
    auth_headers,
):
    await client.post(
        "/api/v1/tasks/",
        headers=auth_headers,
        json={
            "title": "Algorithms",
            "subject": "DSA",
            "description": "Practice problems",
            "priority": "High",
            "estimated_hours": 2,
            "due_date": "2026-08-01",
        },
    )

    await client.post(
        "/api/v1/tasks/",
        headers=auth_headers,
        json={
            "title": "DBMS Revision",
            "subject": "DBMS",
            "description": "Normalize tables",
            "priority": "Medium",
            "estimated_hours": 3,
            "due_date": "2026-08-02",
        },
    )

    response = await client.post(
        "/api/v1/planner/generate",
        headers=auth_headers,
        json={
            "available_hours": 4,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["available_hours"] == 4
    assert len(data["tasks"]) == 2