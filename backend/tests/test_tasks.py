import pytest
@pytest.mark.asyncio
async def test_create_task(client):

    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Task User",
            "email": "task@example.com",
            "password": "password123",
        },
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "task@example.com",
            "password": "password123",
        },
    )

    token = login_response.json()["access_token"]

    response = await client.post(
        "/api/v1/tasks/",
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
@pytest.mark.asyncio
async def test_get_tasks(client):
    
    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Task User",
            "email": "taskuser@example.com",
            "password": "password123",
        },
    )

    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "taskuser@example.com",
            "password": "password123",
        },
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    await client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={
            "title": "Task One",
            "subject": "Backend",
            "description": "First task",
            "priority": "High",
            "estimated_hours": 2,
            "completed": False,
            "due_date": "2026-08-01",
        },
    )

    await client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={
            "title": "Task Two",
            "subject": "Database",
            "description": "Second task",
            "priority": "Medium",
            "estimated_hours": 4,
            "completed": False,
            "due_date": "2026-08-02",
        },
    )

    response = await client.get(
        "/api/v1/tasks/",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Task One"
    assert data[1]["title"] == "Task Two"
@pytest.mark.asyncio
async def test_get_task_by_id(client, auth_headers):
    create_response = await client.post(
        "/api/v1/tasks/",
        headers=auth_headers,
        json={
            "title": "Python Revision",
            "subject": "Python",
            "description": "Revise async programming",
            "priority": "High",
            "estimated_hours": 3,
            "completed": False,
            "due_date": "2026-08-05",
        },
    )

    task_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Python Revision"
    assert data["subject"] == "Python"
@pytest.mark.asyncio
async def test_update_task(client, auth_headers):
    create_response = await client.post(
        "/api/v1/tasks/",
        headers=auth_headers,
        json={
            "title": "Old Title",
            "subject": "Python",
            "description": "Old description",
            "priority": "Low",
            "estimated_hours": 2,
            "completed": False,
            "due_date": "2026-08-01",
        },
    )

    task_id = create_response.json()["id"]

    response = await client.put(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers,
        json={
            "title": "New Title",
            "subject": "FastAPI",
            "description": "Updated description",
            "priority": "High",
            "estimated_hours": 5,
            "completed": True,
            "due_date": "2026-08-10",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Title"
    assert data["subject"] == "FastAPI"
    assert data["priority"] == "High"
    assert data["completed"] is True
@pytest.mark.asyncio
async def test_delete_task(client, auth_headers):
    create_response = await client.post(
        "/api/v1/tasks/",
        headers=auth_headers,
        json={
            "title": "Delete Me",
            "subject": "Testing",
            "description": "Task to be deleted",
            "priority": "Medium",
            "estimated_hours": 2,
            "completed": False,
            "due_date": "2026-08-15",
        },
    )

    task_id = create_response.json()["id"]

    response = await client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Task deleted successfully"
@pytest.mark.asyncio
async def test_get_tasks_without_token(client):
    response = await client.get("/api/v1/tasks/")

    assert response.status_code == 401
@pytest.mark.asyncio
async def test_cannot_access_another_users_task(client, create_user_and_login):
    headers_user1 = await create_user_and_login(
        "User One",
        "user1@example.com",
        "password123",
    )
    response = await client.post(
        "/api/v1/tasks/",
        headers=headers_user1,
        json={
            "title": "Private Task",
            "subject": "Backend",
            "description": "Only User One should access this",
            "priority": "High",
            "estimated_hours": 2,
            "completed": False,
        },
    )
    task_id = response.json()["id"]
    headers_user2 = await create_user_and_login(
        "User Two",
        "user2@example.com",
        "password123",
    )
    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=headers_user2,
    )
    assert response.status_code == 404
@pytest.mark.asyncio
async def test_cannot_update_another_users_task(
    client,
    create_user_and_login,
):
    headers_user1 = await create_user_and_login(
        "User One",
        "user1@example.com",
        "password123",
    )
    response = await client.post(
        "/api/v1/tasks/",
        headers=headers_user1,
        json={
            "title": "Private Task",
            "subject": "Backend",
            "description": "Original",
            "priority": "High",
            "estimated_hours": 2,
            "completed": False,
        },
    )
    task_id = response.json()["id"]
    headers_user2 = await create_user_and_login(
        "User Two",
        "user2@example.com",
        "password123",
    )
    response = await client.put(
        f"/api/v1/tasks/{task_id}",
        headers=headers_user2,
        json={
            "title": "Hacked Task",
            "subject": "Backend",
            "description": "Modified",
            "priority": "Low",
            "estimated_hours": 5,
            "completed": True,
        },
    )
    assert response.status_code == 404
@pytest.mark.asyncio
async def test_cannot_delete_another_users_task(
    client,
    create_user_and_login,
):
    headers_user1 = await create_user_and_login(
        "User One",
        "user1@example.com",
        "password123",
    )

    response = await client.post(
        "/api/v1/tasks/",
        headers=headers_user1,
        json={
            "title": "Private Task",
            "subject": "Backend",
            "description": "Original",
            "priority": "High",
            "estimated_hours": 2,
            "completed": False,
        },
    )

    task_id = response.json()["id"]

    headers_user2 = await create_user_and_login(
        "User Two",
        "user2@example.com",
        "password123",
    )

    response = await client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=headers_user2,
    )
    assert response.status_code == 404