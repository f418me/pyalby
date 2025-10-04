from pathlib import Path

import pytest
import requests
import responses

import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pyalby.utils import make_get_request, make_post_request


@responses.activate
def test_make_get_request_http_error_propagates():
    url = "https://api.getalby.com/test-get"
    responses.add(
        responses.GET,
        url,
        json={"error": "boom"},
        status=500,
    )

    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        make_get_request(url, headers={})

    assert excinfo.value.response.status_code == 500


@responses.activate
def test_make_post_request_http_error_propagates():
    url = "https://api.getalby.com/test-post"
    responses.add(
        responses.POST,
        url,
        json={"error": "boom"},
        status=400,
    )

    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        make_post_request(url, data={}, headers={})

    assert excinfo.value.response.status_code == 400


@responses.activate
def test_make_get_request_connection_error_propagates():
    url = "https://api.getalby.com/test-connection"
    responses.add(
        responses.GET,
        url,
        body=requests.exceptions.ConnectionError("connection failed"),
    )

    with pytest.raises(requests.exceptions.ConnectionError):
        make_get_request(url, headers={})
