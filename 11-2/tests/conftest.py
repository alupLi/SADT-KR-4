import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from faker import Faker

fake = Faker()


@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
def fake_user_data():
    def _generate(age=None):
        return {
            "username": fake.user_name(),
            "age": age if age else fake.random_int(min=19, max=80)
        }
    return _generate


@pytest.fixture
async def cleanup_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
        await client.delete("/users")


@pytest.fixture
def faker_instance():
    return fake