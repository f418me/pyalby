import aiohttp
import logging


def _mask_sensitive_headers(headers):
    """Return a copy of headers with sensitive values like Authorization redacted."""
    if not headers:
        return headers

    masked_headers = {}
    for key, value in headers.items():
        if key.lower() == "authorization":
            masked_headers[key] = "***REDACTED***"
        else:
            masked_headers[key] = value
    return masked_headers


def _mask_sensitive_data(data):
    """Return a copy of data with token-like fields redacted before logging."""
    if not isinstance(data, dict):
        return data

    masked_data = {}
    for key, value in data.items():
        if any(sensitive in key.lower() for sensitive in ("token", "secret", "authorization")):
            masked_data[key] = "***REDACTED***"
        else:
            masked_data[key] = value
    return masked_data


async def make_async_get_request(url, headers):
    """
    Make an asynchronous GET request to the specified URL.
    
    This utility function handles async HTTP GET requests with proper session management,
    error handling, and logging. It's used internally by the async API classes.
    
    Args:
        url (str): The URL to make the request to
        headers (dict): Headers to include in the request
        
    Returns:
        dict: JSON response from the API
        
    Raises:
        aiohttp.ClientResponseError: For HTTP 4xx/5xx responses
        aiohttp.ClientConnectionError: For connection issues
        aiohttp.ServerTimeoutError: For timeout issues
        aiohttp.ClientError: For other aiohttp-related errors
        Exception: For unexpected errors
        
    Example:
        ```python
        import asyncio
        from pyalby.async_utils import make_async_get_request
        
        async def example():
            headers = {"Authorization": "Bearer your_token"}
            response = await make_async_get_request(
                "https://api.example.com/data", 
                headers
            )
            print(response)
            
        asyncio.run(example())
        ```
    """
    logging.info(
        "Calling GET API URL: %s with headers: %s",
        url,
        _mask_sensitive_headers(headers),
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                logging.debug("Response Status Code: %s", response.status)
                return await response.json()
    except aiohttp.ClientResponseError as http_err:
        # aiohttp.ClientResponseError doesn't have a response attribute like requests
        # The error message already contains the status and reason
        logging.error(f"HTTP error occurred: {http_err}")
        raise
    except aiohttp.ClientConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
        raise
    except aiohttp.ServerTimeoutError as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
        raise
    except aiohttp.ClientError as client_err:
        logging.error(f"Client error occurred: {client_err}")
        raise
    except Exception as err:
        logging.error(f"An unexpected error occurred: {err}")
        raise


async def make_async_post_request(url, data, headers):
    """
    Make an asynchronous POST request to the specified URL.
    
    This utility function handles async HTTP POST requests with proper session management,
    error handling, and logging. It automatically filters out None values from the data
    and is used internally by the async API classes.
    
    Args:
        url (str): The URL to make the request to
        data (dict): Data to send in the request body as JSON
        headers (dict): Headers to include in the request
        
    Returns:
        dict: JSON response from the API
        
    Raises:
        aiohttp.ClientResponseError: For HTTP 4xx/5xx responses
        aiohttp.ClientConnectionError: For connection issues
        aiohttp.ServerTimeoutError: For timeout issues
        aiohttp.ClientError: For other aiohttp-related errors
        Exception: For unexpected errors
        
    Example:
        ```python
        import asyncio
        from pyalby.async_utils import make_async_post_request
        
        async def example():
            headers = {"Authorization": "Bearer your_token", "Content-Type": "application/json"}
            data = {"amount": 1000, "description": "Test payment"}
            response = await make_async_post_request(
                "https://api.example.com/payments", 
                data,
                headers
            )
            print(response)
            
        asyncio.run(example())
        ```
    """
    try:
        # Remove any optional arguments with None values
        data = {k: v for k, v in data.items() if v is not None}
        logging.info(
            "Calling POST API URL: %s with headers: %s and data: %s",
            url,
            _mask_sensitive_headers(headers),
            _mask_sensitive_data(data),
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                response.raise_for_status()
                logging.debug("Response Status Code: %s", response.status)
                return await response.json()
    except aiohttp.ClientResponseError as http_err:
        # aiohttp.ClientResponseError doesn't have a response attribute like requests
        # The error message already contains the status and reason
        logging.error(f"HTTP error occurred: {http_err}")
        raise
    except aiohttp.ClientConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
        raise
    except aiohttp.ServerTimeoutError as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
        raise
    except aiohttp.ClientError as client_err:
        logging.error(f"Client error occurred: {client_err}")
        raise
    except Exception as err:
        logging.error(f"An unexpected error occurred: {err}")
        raise
