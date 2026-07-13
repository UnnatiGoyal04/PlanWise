import pytest
@pytest.mark.asyncio
async def test_create_task(client):

    await client.post(
        "/auth/register",
        json={
            "name": "Task User",
            "email": "task@example.com",
            "password": "password123",
        },
    )

    login_response = await client.post(
        "/auth/login",
        data={
            "username": "task@example.com",
            "password": "password123",
        },
    )

    token = login_response.json()["access_token"]

    response = await client.post(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Learn FastAPI",
            "subject": "Backend",
            "description": "Testing task creation",
            "priority": "High",
            "estimated_hours": 5,
            "due_date": "2026-08-01",
        },
    )

    print(response.status_code)
    print(response.json())