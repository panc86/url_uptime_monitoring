# pylint: disable=redefined-outer-name
import pytest
import datetime
import re
import producer


class TestResponse(object):
    # default response attributes the servive uses
    status_code = 200
    elapsed = datetime.timedelta(microseconds=420)
    text = 'fake response text'


@pytest.fixture
def response():
    # a valid url should return 200
    return TestResponse()


@pytest.fixture
def pattern():
    return re.compile(r'\bresponse\b', re.I)


@pytest.fixture
def pattern_is_none():
    # If no regex pattern returned value is 0
    return None


def test_get_status_code(response):
    assert hasattr(response, "status_code")
    assert response.status_code == 200


def test_get_elapsed_seconds(response):
    assert hasattr(response, "elapsed")
    assert type(response.elapsed) == datetime.timedelta
    assert response.elapsed.total_seconds() == 0.00042


def test_get_matches_count(response, pattern):
    assert hasattr(response, "text")
    assert response.text == 'fake response text'
    assert producer.get_matches_count(response, pattern) == 1


def test_get_matches_count_missing_pattern(response, pattern_is_none):
    assert producer.get_matches_count(response, pattern_is_none) == 0


# TODO
#def test_get_payload(url, pattern):
#    pass


# TODO
#def test_monitor():
#    pass
