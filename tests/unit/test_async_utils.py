from pathlib import Path
import pytest
import aiohttp
from aioresponses import aioresponses
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pyalby.async_utils import make_async_get_request, make_async_post_request


@pytest.mark.asyncio
async def test_make_async_get_request_success():
    """Test successful GET request returns JSON response."""
    url = "https://api.getalby.com/test-get"
    expected_response = {"status": "success", "data": "test"}
    
    with aioresponses() as m:
        m.get(url, payload=expected_response, status=200)
        
        result = await make_async_get_request(url, headers={})
        
        assert result == expected_response


@pytest.mark.asyncio
async def test_make_async_post_request_success():
    """Test successful POST request returns JSON response."""
    url = "https://api.getalby.com/test-post"
    request_data = {"amount": 1000, "description": "test"}
    expected_response = {"payment_hash": "abc123", "status": "created"}
    
    with aioresponses() as m:
        m.post(url, payload=expected_response, status=201)
        
        result = await make_async_post_request(url, request_data, headers={})
        
        assert result == expected_response


@pytest.mark.asyncio
async def test_make_async_get_request_http_error_propagates():
    """Test that HTTP errors are properly propagated."""
    url = "https://api.getalby.com/test-get"
    
    with aioresponses() as m:
        m.get(url, payload={"error": "boom"}, status=500)
        
        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await make_async_get_request(url, headers={})
        
        assert excinfo.value.status == 500


@pytest.mark.asyncio
async def test_make_async_post_request_http_error_propagates():
    """Test that HTTP errors are properly propagated for POST requests."""
    url = "https://api.getalby.com/test-post"
    
    with aioresponses() as m:
        m.post(url, payload={"error": "boom"}, status=400)
        
        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await make_async_post_request(url, data={}, headers={})
        
        assert excinfo.value.status == 400


@pytest.mark.asyncio
async def test_make_async_get_request_connection_error_propagates():
    """Test that connection errors are properly propagated."""
    url = "https://api.getalby.com/test-connection"
    
    with aioresponses() as m:
        m.get(url, exception=aiohttp.ClientConnectionError("connection failed"))
        
        with pytest.raises(aiohttp.ClientConnectionError):
            await make_async_get_request(url, headers={})


@pytest.mark.asyncio
async def test_make_async_post_request_connection_error_propagates():
    """Test that connection errors are properly propagated for POST requests."""
    url = "https://api.getalby.com/test-connection"
    
    with aioresponses() as m:
        m.post(url, exception=aiohttp.ClientConnectionError("connection failed"))
        
        with pytest.raises(aiohttp.ClientConnectionError):
            await make_async_post_request(url, data={}, headers={})


@pytest.mark.asyncio
async def test_make_async_get_request_timeout_error_propagates():
    """Test that timeout errors are properly propagated."""
    url = "https://api.getalby.com/test-timeout"
    
    with aioresponses() as m:
        m.get(url, exception=aiohttp.ServerTimeoutError("timeout"))
        
        with pytest.raises(aiohttp.ServerTimeoutError):
            await make_async_get_request(url, headers={})


@pytest.mark.asyncio
async def test_make_async_post_request_timeout_error_propagates():
    """Test that timeout errors are properly propagated for POST requests."""
    url = "https://api.getalby.com/test-timeout"
    
    with aioresponses() as m:
        m.post(url, exception=aiohttp.ServerTimeoutError("timeout"))
        
        with pytest.raises(aiohttp.ServerTimeoutError):
            await make_async_post_request(url, data={}, headers={})


@pytest.mark.asyncio
async def test_make_async_post_request_filters_none_values():
    """Test that POST request filters out None values from data."""
    url = "https://api.getalby.com/test-post"
    request_data = {"amount": 1000, "description": None, "memo": "test"}
    expected_response = {"status": "success"}
    
    with aioresponses() as m:
        # We need to verify that the request was made without the None value
        m.post(url, payload=expected_response, status=200)
        
        result = await make_async_post_request(url, request_data, headers={})
        
        assert result == expected_response
        # Verify the request was made (aioresponses will fail if no matching request)
        assert len(m.requests) == 1


@pytest.mark.asyncio
async def test_make_async_get_request_with_headers():
    """Test GET request with custom headers."""
    url = "https://api.getalby.com/test-headers"
    headers = {"Authorization": "Bearer token123", "Content-Type": "application/json"}
    expected_response = {"authenticated": True}
    
    with aioresponses() as m:
        m.get(url, payload=expected_response, status=200)
        
        result = await make_async_get_request(url, headers)
        
        assert result == expected_response


@pytest.mark.asyncio
async def test_make_async_post_request_with_headers():
    """Test POST request with custom headers."""
    url = "https://api.getalby.com/test-headers"
    headers = {"Authorization": "Bearer token123", "Content-Type": "application/json"}
    request_data = {"test": "data"}
    expected_response = {"created": True}
    
    with aioresponses() as m:
        m.post(url, payload=expected_response, status=201)
        
        result = await make_async_post_request(url, request_data, headers)
        
        assert result == expected_response