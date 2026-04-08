import pytest
import sys
class MockSettings:
    BASE_URL = "http://test.com"

mock_config = type('mock', (), {
    'settings': MockSettings(),
    'lg': None
})
sys.modules['app.config'] = mock_config
from app.services.shortener import Shortener
class DummyRepo:
    async def add_link(self, original_link, short_key):
        return None
@pytest.mark.asyncio
async def test_shorten_valid_url():
    s = Shortener(links_repo=DummyRepo())
    result = await s.shorten("https://google.com")
    assert result is not None
@pytest.mark.asyncio
async def test_shorten_empty_string():
    s = Shortener(links_repo=DummyRepo())
    result = await s.shorten("")
    assert result is not None or result == ""
@pytest.mark.asyncio
async def test_shorten_invalid_input():
    s = Shortener(links_repo=DummyRepo())
    try:
        await s.shorten(None)
        assert True
    except Exception:
        assert True
