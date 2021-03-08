# pylint: disable=redefined-outer-name
import pytest
import os
import re
import time
import datetime
import producer
from requests import Response
from kafka import KafkaProducer


class TestResponse(object):
    # default response attributes the servive uses
    status_code = 200
    elapsed = datetime.timedelta(microseconds=420)
    text = 'fake response text'


@pytest.fixture
def url():
    return 'http://www.example.com'


@pytest.fixture
def bad_url():
    return 'http://www.example.'


@pytest.fixture
def response():
    # a valid url should return 200
    return TestResponse()


@pytest.fixture
def regex():
    return re.compile(r"\bresponse\b", re.IGNORECASE)


@pytest.fixture
def text(response):
    return response.text


@pytest.fixture(scope="session")
def client():
    client = KafkaProducer(
            api_version=(2,0,1),
            bootstrap_servers=["172.17.0.1:9092"],
        )
    time.sleep(1)
    return client


def test_get_status_code(response):
    assert hasattr(response, "status_code")
    assert response.status_code == 200


def test_get_elapsed_seconds(response):
    assert hasattr(response, "elapsed")
    assert type(response.elapsed) == datetime.timedelta
    assert response.elapsed.total_seconds() == 0.00042


def test_get_matches_count(text, regex):
    assert producer.get_matches_count(text, regex) == 1


def test_get_response(url):
    assert isinstance(producer.get_response(url), Response)


def test_get_response_raise(bad_url):
    with pytest.raises(SystemExit):
        producer.get_response(bad_url)


def test_get_payload(response):
    payload = producer.get_payload(response)
    assert len(payload) == 3
    assert "created_at" in payload
    assert isinstance(payload["created_at"], str)


def test_client_connected(client):
    assert client.bootstrap_connected()
