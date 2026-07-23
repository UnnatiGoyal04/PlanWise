import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_login_user(client):

    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "password123",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "login@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0

@pytest.mark.asyncio
async def test_get_current_user(client):

    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Current User",
            "email": "current@example.com",
            "password": "password123",
        },
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "current@example.com",
            "password": "password123",
        },
    )

    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Current User"
    assert data["email"] == "current@example.com"
    assert "id" in data
    assert "created_at" in data