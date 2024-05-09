import requests
import logging

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


def make_post_request(url, data, headers):
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
