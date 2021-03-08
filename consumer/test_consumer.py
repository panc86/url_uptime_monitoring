# pylint: disable=redefined-outer-name
import pytest
import os
import consumer
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


@pytest.fixture
def payload():
    return dict(
        created_at="2021-03-08T17:49:12.629564",
        status_code=420,
        elapsed_seconds=0.0420,
        regex_matches=0,
        regex_pattern="hello"
    )


@pytest.fixture
def bad_payload():
    return dict(
        status_=420, # wrong key name
        elapsed_seconds=0.0420,
        regex_pattern=None
    )


@pytest.fixture
def incomplete_payload():
    return dict(
        status_code=420,
        elapsed_seconds=0.0420,
        regex_pattern=None
    )


@pytest.fixture(scope="session")
def test_db():
    return consumer.setup_db(os.environ['DB_URI_TEST'])


@pytest.fixture(scope="session")
def test_session(test_db):
    return consumer.init_session(test_db)


@pytest.fixture(scope="session")
def consumer_client():
    bootstrap_server = os.environ['BOOTSTRAP_SERVER']
    topic = 'test_' + os.environ['TOPIC_ID']
    return consumer.init_consumer_client(bootstrap_server, topic)


def test_create_message_model(payload):
    msg = consumer.create_message_model(payload)
    # Expected in a good message
    assert hasattr(msg, "created_at")
    assert hasattr(msg, "status_code")
    assert hasattr(msg, "elapsed_seconds")
    assert hasattr(msg, "regex_matches")
    assert hasattr(msg, "regex_pattern")


def test_create_message_model_with_bad_payload(bad_payload):
    # Expected in a bad message
    with pytest.raises(TypeError):
        consumer.Message(**bad_payload)


def test_create_message_model_with_incomplete_payload(incomplete_payload):
    # Expected in a incomplete message
    with pytest.raises(TypeError):
        assert consumer.Message(**incomplete_payload)


def test_setup_db(test_db):
    # DB Engin instance expected
    assert isinstance(test_db, Engine)
    # Messages table expected
    assert test_db.table_names() == ["messages"]


def test_init_session(test_session):
    # Session instance expected
    assert isinstance(test_session, Session)


def test_db_empty(test_session):
    # .first() returns None if DB in session is empty
    assert test_session.query(consumer.Message).first() is None


def test_insert_to_db(payload, test_session):
    # insert first record
    consumer.insert_to_db(consumer.Message(**payload), test_session)
    # query first record
    first_entry = test_session.query(consumer.Message).first()
    # assert if first record
    assert first_entry.id == 1


def test_init_consumer_client(consumer_client):
    # Is client online?
    assert consumer_client._closed is False
    assert consumer_client.subscription() == {'test_flood'}
