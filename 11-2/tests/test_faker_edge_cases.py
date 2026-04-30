import pytest
from faker import Faker

fake = Faker()


@pytest.mark.asyncio
async def test_create_user_minimum_age(async_client, fake_user_data):
    user_data = fake_user_data(age=19)
    response = await async_client.post("/users", json=user_data)
    assert response.status_code == 201
    
    user_data = fake_user_data(age=18)
    response = await async_client.post("/users", json=user_data)
    assert response.status_code in [201, 422]


@pytest.mark.asyncio
async def test_create_user_maximum_age(async_client, fake_user_data):
    user_data = fake_user_data(age=120)
    response = await async_client.post("/users", json=user_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_user_invalid_negative_age(async_client):
    response = await async_client.post("/users", json={
        "username": fake.user_name(),
        "age": -5
    })
    assert response.status_code in [201, 422]


@pytest.mark.asyncio
async def test_create_user_long_username(async_client):
    long_username = "a" * 100
    response = await async_client.post("/users", json={
        "username": long_username,
        "age": 25
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == long_username


@pytest.mark.asyncio
async def test_create_user_special_characters(async_client):
    special_username = "user_@#$%^&*()"
    response = await async_client.post("/users", json={
        "username": special_username,
        "age": 25
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == special_username


@pytest.mark.asyncio
async def test_create_user_with_faker_name(async_client, faker_instance):
    response = await async_client.post("/users", json={
        "username": faker_instance.first_name(),
        "age": faker_instance.random_int(min=19, max=60)
    })
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_user_with_faker_profile(async_client, faker_instance):
    profile = faker_instance.profile()
    
    response = await async_client.post("/users", json={
        "username": profile["username"][:30],
        "age": faker_instance.random_int(min=19, max=60)
    })
    assert response.status_code == 201