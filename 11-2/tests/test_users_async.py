import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_user_success(async_client, fake_user_data):
    user_data = fake_user_data()
    
    response = await async_client.post("/users", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["username"] == user_data["username"]
    assert data["age"] == user_data["age"]
    assert isinstance(data["id"], int)


@pytest.mark.asyncio
async def test_get_existing_user(async_client, fake_user_data):
    create_response = await async_client.post("/users", json=fake_user_data())
    user_id = create_response.json()["id"]
    
    response = await async_client.get(f"/users/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert "username" in data
    assert "age" in data


@pytest.mark.asyncio
async def test_get_nonexistent_user(async_client):
    response = await async_client.get("/users/99999")
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_existing_user(async_client, fake_user_data):
    create_response = await async_client.post("/users", json=fake_user_data())
    user_id = create_response.json()["id"]
    
    response = await async_client.delete(f"/users/{user_id}")
    
    assert response.status_code == 204
    
    get_response = await async_client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_user(async_client):
    response1 = await async_client.delete("/users/99999")
    assert response1.status_code == 404
    
    response2 = await async_client.delete("/users/99999")
    assert response2.status_code == 404


@pytest.mark.asyncio
async def test_create_multiple_users_async(async_client, fake_user_data):
    users_data = [fake_user_data() for _ in range(3)]
    
    responses = []
    for user_data in users_data:
        response = await async_client.post("/users", json=user_data)
        responses.append(response)
    
    for response, user_data in zip(responses, users_data):
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["age"] == user_data["age"]


@pytest.mark.asyncio
async def test_create_and_delete_multiple_users(async_client, fake_user_data):
    user_ids = []
    
    for _ in range(3):
        response = await async_client.post("/users", json=fake_user_data())
        user_ids.append(response.json()["id"])
    
    for user_id in user_ids:
        response = await async_client.delete(f"/users/{user_id}")
        assert response.status_code == 204
    
    for user_id in user_ids:
        get_response = await async_client.get(f"/users/{user_id}")
        assert get_response.status_code == 404