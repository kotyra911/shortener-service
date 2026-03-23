import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import AsyncSessionLocal, engine
from collections.abc import AsyncGenerator
from app.models.base import Base
from app.config import settings
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture(scope="session",autouse=True)
async def setup():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
async def test_shorten_link():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=settings.BASE_URL,
        ) as ac:

        link_without_http = {
            "original_link": "google.com",
        }

        response = await ac.post("/shorten", json=link_without_http)

        assert response.status_code == 200

        r_data = response.json()

        assert "short_link" in r_data
        assert isinstance(r_data["short_link"], str)

        short_key = r_data["short_link"].removeprefix(settings.BASE_URL)

        assert len(short_key) == 6


@pytest.mark.asyncio
async def test_shorten_link_with_http():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=settings.BASE_URL,
    ) as ac:

        link_with_http = {
            "original_link": "https://www.google.com/",
        }

        response = await ac.post("/shorten", json=link_with_http)

        assert response.status_code == 200

        r_data = response.json()

        assert "short_link" in r_data

        short_key = r_data["short_link"].removeprefix(settings.BASE_URL)

        assert len(short_key) == 6


@pytest.mark.asyncio
async def test_redirect_user():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=settings.BASE_URL,
        follow_redirects=False,
    ) as ac:

        link_without_http = {
            "original_link": "https://www.google.com/",
        }

        response = await ac.post("/shorten", json=link_without_http)

        r_data = response.json()

        short_key = r_data["short_link"].removeprefix(settings.BASE_URL)

        redirect_response = await ac.get(f"/{short_key}",follow_redirects=False)

        assert redirect_response.headers["location"] == "https://www.google.com/"


@pytest.mark.asyncio
async def test_redirect_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=settings.BASE_URL,
        follow_redirects=False,
    ) as ac:

        response = await ac.get("/unknown-request-test")

        assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_link_stats():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=settings.BASE_URL,
        follow_redirects=False,
    ) as ac:

        response = await ac.post(
            "/shorten",
            json={"original_link": "https://www.google.com/"},
        )
        assert response.status_code == 200

        short_link = response.json()["short_link"]
        short_key = short_link.removeprefix(settings.BASE_URL)

        for _ in range(3):
            await ac.get(f"/{short_key}")

        stats_response = await ac.get(f"/stats/{short_key}")

        assert stats_response.status_code == 200

        data = stats_response.json()

        assert "link_clicks" in data
        assert data["link_clicks"] == 3


@pytest.mark.asyncio
async def test_get_link_stats_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=settings.BASE_URL,
    ) as ac:

        response = await ac.get("/stats/unknown-request-test")

        assert response.status_code == 404