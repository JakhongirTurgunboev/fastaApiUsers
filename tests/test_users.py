import pytest
from httpx import AsyncClient

from api.main import app
from database.database import SessionLocal


@pytest.fixture
def db():
    return SessionLocal()


@pytest.mark.asyncio
async def test_create_user(db):
    # Implement your test logic here
    pass


@pytest.mark.asyncio
async def test_read_user(db):
    # Implement your test logic here
    pass
