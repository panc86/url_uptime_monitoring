# pylint: disable=redefined-outer-name
import pytest
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
# to test
from consumer import setup_db, insert_to_db, create_message_model, Message


def payload_valid():
    return dict(
        created_at=datetime.utcnow(), # sqlite does not accept strings as dates
        status_code=420,
        elapsed_seconds=0.0420,
        regex_matches=0,
        regex_pattern="hello"
    )


def payload_invalid():
    return dict(
        status_=420, # wrong key name
        elapsed_seconds=0.0420,
        regex_pattern=None
    )


def payload_incomplete():
    return dict(
        elapsed_seconds=0.0420,
        regex_pattern=None
    )


# test db uri
URI = "sqlite:///:memory:"


def test_setup_db():
    db, make_session = setup_db(URI)
    s = make_session()
    # DB Engin instance expected
    assert isinstance(db, Engine)
    # Messages table expected
    assert db.table_names() == ["messages"], "Should contain `messages` table."
    # Session instance expected
    assert isinstance(s, Session), "Should be Session class type."


def test_create_message_model():
    # load good message
    message = create_message_model(payload_valid())
    # Expected in a good message
    assert hasattr(message, "created_at")
    assert hasattr(message, "status_code")
    assert hasattr(message, "elapsed_seconds")
    assert hasattr(message, "regex_matches")
    assert hasattr(message, "regex_pattern")


def test_create_message_model_with_bad_payload():
    # Expected in a bad message
    with pytest.raises(TypeError):
        Message(**payload_invalid())


def test_create_message_model_with_incomplete_payload():
    # Expected in a incomplete message
    with pytest.raises(TypeError):
        Message(**payload_incomplete())


def test_db_empty():
    _, make_session = setup_db(URI)
    s = make_session()
    # .first() returns None if DB in session is empty
    assert s.query(Message).first() is None, "Should not exisis."


def test_insert_to_db():
    _, make_session = setup_db(URI)
    s = make_session()
    # insert first record
    insert_to_db(Message(**payload_valid()), s)
    # query first record
    first_entry = s.query(Message).first()
    # assert if first record
    assert first_entry.id == 1, "Should be 1."


def test_db_recreation():
    db, make_session = setup_db(URI)
    s = make_session()
    assert s.query(Message).first() is None, "Should not exisis."
