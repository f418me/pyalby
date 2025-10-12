import aiohttp
import logging


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
    logging.info(f"Calling GET API URL: {url} with headers: {headers}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                logging.debug(f"Response Status Code: {response.status}")
                logging.debug(f"Response Headers: {response.headers}")
                response_text = await response.text()
                logging.debug(f"Response Body: {response_text}")
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
    logging.info(f"Calling POST API URL: {url} with headers: {headers} and data: {data}")
    try:
        # Remove any optional arguments with None values
        data = {k: v for k, v in data.items() if v is not None}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                response.raise_for_status()
                logging.debug(f"Response Status Code: {response.status}")
                logging.debug(f"Response Headers: {response.headers}")
                response_text = await response.text()
                logging.debug(f"Response Body: {response_text}")
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