import pytest
import sys
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError

# Mock settings before importing Shortener
class MockSettings:
    BASE_URL = "http://127.0.0.1:8000/"

mock_config = type('mock', (), {
    'settings': MockSettings(),
    'lg': MagicMock()
})
sys.modules['app.config'] = mock_config

from app.services.shortener import Shortener


class MockLinkRepository:
    """Mock repository for testing"""
    def __init__(self, raise_integrity_error=False):
        self.raise_integrity_error = raise_integrity_error
        self.add_link_calls = []

    async def add_link(self, original_link: str, short_key: str) -> None:
        self.add_link_calls.append((original_link, short_key))
        if self.raise_integrity_error:
            raise IntegrityError("Duplicate key", None, None)


# Test valid HTTPS URL
@pytest.mark.asyncio
async def test_shorten_valid_https_url():
    """Test shortening a valid HTTPS URL"""
    repo = MockLinkRepository()
    db = AsyncMock()
    shortener = Shortener(links_repo=repo, db=db)
    
    result = await shortener.shorten("https://www.google.com")
    
    assert result is not None
    assert result.startswith("http://127.0.0.1:8000/")
    assert len(result) == len("http://127.0.0.1:8000/") + 6
    db.commit.assert_called_once()


# Test valid HTTP URL
@pytest.mark.asyncio
async def test_shorten_valid_http_url():
    """Test shortening a valid HTTP URL"""
    repo = MockLinkRepository()
    db = AsyncMock()
    shortener = Shortener(links_repo=repo, db=db)
    
    result = await shortener.shorten("http://github.com")
    
    assert result is not None
    assert result.startswith("http://127.0.0.1:8000/")
    assert len(result) == len("http://127.0.0.1:8000/") + 6


# Test URL without protocol
@pytest.mark.asyncio
async def test_shorten_url_without_protocol():
    """Test shortening a URL without http/https protocol"""
    repo = MockLinkRepository()
    db = AsyncMock()
    shortener = Shortener(links_repo=repo, db=db)
    
    result = await shortener.shorten("example.com")
    
    assert result is not None
    assert result.startswith("http://127.0.0.1:8000/")
    assert repo.add_link_calls[0][0] == "http://example.com"


# Test generated short key length
@pytest.mark.asyncio
async def test_shorten_generates_6_char_key():
    """Test that shorten generates a 6-character short key"""
    repo = MockLinkRepository()
    db = AsyncMock()
    shortener = Shortener(links_repo=repo, db=db)
    
    result = await shortener.shorten("https://github.com")
    
    short_key = result.replace("http://127.0.0.1:8000/", "")
    assert len(short_key) == 6
    assert short_key.isalnum()


# Test HTTP check method
@pytest.mark.asyncio
async def test_http_check_adds_protocol():
    """Test _http_check adds http:// to plain domains"""
    repo = MockLinkRepository()
    shortener = Shortener(links_repo=repo)
    
    result = shortener._http_check("example.com")
    assert result == "http://example.com"


@pytest.mark.asyncio
async def test_http_check_preserves_https():
    """Test _http_check preserves https URLs"""
    repo = MockLinkRepository()
    shortener = Shortener(links_repo=repo)
    
    result = shortener._http_check("https://example.com")
    assert result == "https://example.com"


# Test URL composition
@pytest.mark.asyncio
async def test_compose_url_builds_correct_url():
    """Test _compose_url builds correct short URL"""
    repo = MockLinkRepository()
    shortener = Shortener(links_repo=repo)
    
    result = shortener._compose_url("abc123")
    assert result == "http://127.0.0.1:8000/abc123"


# Test generate_random_string
@pytest.mark.asyncio
async def test_generate_random_string_length():
    """Test _generate_random_string produces 6-character strings"""
    repo = MockLinkRepository()
    shortener = Shortener(links_repo=repo)
    
    result = shortener._generate_random_string()
    assert len(result) == 6
    assert result.isalnum()


# Test repository called correctly
@pytest.mark.asyncio
async def test_shorten_calls_repository_with_correct_params():
    """Test that shorten calls repository correctly"""
    repo = MockLinkRepository()
    db = AsyncMock()
    shortener = Shortener(links_repo=repo, db=db)
    
    original_link = "https://example.com/path"
    result = await shortener.shorten(original_link)
    
    assert len(repo.add_link_calls) > 0
    stored_link, short_key = repo.add_link_calls[0]
    assert stored_link == original_link
    assert len(short_key) == 6


# Test with complex URLs
@pytest.mark.asyncio
async def test_shorten_with_complex_urls():
    """Test shortening various complex URLs"""
    repo = MockLinkRepository()
    db = AsyncMock()
    shortener = Shortener(links_repo=repo, db=db)
    
    test_urls = [
        "https://github.com/user/repo/issues/123",
        "https://example.com/path?query=value&other=param",
        "https://subdomain.example.co.uk/api/v1/endpoint",
    ]
    
    for url in test_urls:
        result = await shortener.shorten(url)
        assert result is not None
        assert result.startswith("http://127.0.0.1:8000/")


# Integration test
@pytest.mark.asyncio
async def test_shorten_complete_flow():
    """Integration test for complete shorten flow"""
    repo = MockLinkRepository()
    db = AsyncMock()
    shortener = Shortener(links_repo=repo, db=db)
    
    original = "github.com"
    result = await shortener.shorten(original)
    
    assert result.startswith("http://127.0.0.1:8000/")
    short_key = result.replace("http://127.0.0.1:8000/", "")
    assert len(short_key) == 6
    assert repo.add_link_calls[0][0] == "http://github.com"
    assert repo.add_link_calls[0][1] == short_key
    db.commit.assert_called_once()
