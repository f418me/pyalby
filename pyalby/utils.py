import requests
import logging
import aiohttp
import logging
import asyncio


def make_get_request(url, headers):
    logging.info(f"Calling GET API URL: {url} with headers: {headers}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.debug(f"Response Status Code: {response.status_code}")
        logging.debug(f"Response Headers: {response.headers}")
        logging.debug(f"Response Body: {response.text}")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"An error occurred: {req_err}")
    except Exception as err:
        logging.error(f"An unexpected error occurred: {err}")

    return err


async def make_async_get_request(url, headers):
    logging.info(f"Calling async GET API URL: {url} with headers: {headers}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                text = await response.text()
                logging.debug(f"Response Status Code: {response.status}")
                logging.debug(f"Response Headers: {response.headers}")
                logging.debug(f"Response Body: {text}")
                return await response.json()

    except aiohttp.ClientResponseError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - Response: {await response.text()}")
    except aiohttp.ClientConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except asyncio.TimeoutError as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except aiohttp.ClientError as req_err:
        logging.error(f"An error occurred: {req_err}")
    except Exception as err:
        logging.error(f"An unexpected error occurred: {err}")
    return err


def make_async_post_request(url, data, headers):
    logging.info(f"Calling POST API URL: {url} with headers: {headers} and data: {data}")
    try:
        # Remove any optional arguments with None values
        data = {k: v for k, v in data.items() if v is not None}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        logging.debug(f"Response Status Code: {response.status_code}")
        logging.debug(f"Response Headers: {response.headers}")
        logging.debug(f"Response Body: {response.text}")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"An error occurred: {req_err}")
    except Exception as err:
        logging.error(f"An unexpected error occurred: {err}")

    return err


async def make_post_request(url, data, headers):
    logging.info(f"Calling async POST API URL: {url} with headers: {headers} and data: {data}")
    try:
        # Remove any optional arguments with None values
        data = {k: v for k, v in data.items() if v is not None}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                response.raise_for_status()
                text = await response.text()
                logging.debug(f"Response Status Code: {response.status}")
                logging.debug(f"Response Headers: {response.headers}")
                logging.debug(f"Response Body: {text}")
                return await response.json()

    except aiohttp.ClientResponseError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - Response: {await response.text()}")
    except aiohttp.ClientConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except asyncio.TimeoutError as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except aiohttp.ClientError as req_err:
        logging.error(f"An error occurred: {req_err}")
    except Exception as err:
        logging.error(f"An unexpected error occurred: {err}")
    return err

