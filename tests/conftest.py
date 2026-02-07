"""Test configuration."""

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost:5432/test_db"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
async def setup_database():
    """Create test database tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(setup_database) -> AsyncGenerator[AsyncSession, None]:
    """Get test database session."""
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Get test client."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()
