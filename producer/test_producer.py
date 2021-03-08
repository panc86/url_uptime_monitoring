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


url = 'http://www.example.com'
bad_url = 'http://www.example.'


def test_get_status_code():
    response = TestResponse()
    assert hasattr(response, "status_code")
    assert response.status_code == 200


def test_get_elapsed_seconds():
    response = TestResponse()
    assert hasattr(response, "elapsed")
    assert type(response.elapsed) == datetime.timedelta
    assert response.elapsed.total_seconds() == 0.00042


def test_get_matches_count():
    response = TestResponse()
    regex = re.compile(r"\bresponse\b", re.IGNORECASE)
    assert producer.get_matches_count(response.text, regex) == 1


def test_get_response():
    assert isinstance(producer.get_response(url), Response)


def test_get_response_raise():
    with pytest.raises(SystemExit):
        producer.get_response(bad_url)


def test_get_payload():
    response = TestResponse()
    payload = producer.get_payload(response)
    assert len(payload) == 3
    assert "created_at" in payload
    assert isinstance(payload["created_at"], str)


def test_client_connected():
    client = KafkaProducer(
        api_version=(2,0,1),
        bootstrap_servers=[os.environ['BOOTSTRAP_SERVER']],
    )
    time.sleep(1)
    assert client.bootstrap_connected()
