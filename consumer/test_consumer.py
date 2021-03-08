# pylint: disable=redefined-outer-name
import pytest
import os
import consumer


@pytest.fixture
def payload():
    return dict(
        status_code=420,
        elapsed_seconds=0.0420,
        regex_matches=0,
        regex_pattern=None
    )


@pytest.fixture
def bad_payload():
    return dict(
        status_=420, # wrong key name
        elapsed_seconds=0.0420,
        # missing regex_matches
        regex_pattern=None
    )


@pytest.fixture
def host():
    return os.environ['HOST']


@pytest.fixture
def topic_id():
    return 'test_' + os.environ['TOPIC_ID']


@pytest.fixture
def uri():
    return os.environ['DB_URI']+'_test'


@pytest.fixture
def message(payload):
    return consumer.Message(**payload)


def test_create_message_model(message):
    assert hasattr(message, "status_code")
    assert hasattr(message, "elapsed_seconds")
    assert hasattr(message, "regex_matches")
    assert hasattr(message, "regex_pattern")


# def test_setup_db():
#     pass


# def test_init_session():
#     pass


# def test_insert_to_db():
#     pass


# def test_init_consumer_client():
#     pass
