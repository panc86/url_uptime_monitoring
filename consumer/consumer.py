import logging
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from kafka import KafkaConsumer
import json


# initialize logger
logger = logging.getLogger("consumer")


# RDBMS blueprints for DB creation
base = declarative_base()


# DB model
class Message(base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True) # autogenerated at insert
    created_at = Column("created_at", DateTime())
    status_code = Column('status_code', Integer())
    elapsed_seconds = Column('elapsed_seconds', Float())
    regex_matches = Column('regex_matches', Integer())
    regex_pattern = Column('regex_pattern', String(100))

    def __init__(self, created_at, status_code, elapsed_seconds, regex_matches=0, regex_pattern=None):
        self.created_at = created_at
        self.status_code = status_code
        self.elapsed_seconds = elapsed_seconds
        self.regex_matches = regex_matches
        self.regex_pattern = regex_pattern

    def __repr__(self):
        return f'<Message #{self.id}>'


def setup_db(uri: str):
    """
    Create SQLAlchemy DB engine and return a DB session
    """
    db = create_engine(uri)
    # drop metadata if exists
    base.metadata.drop_all(db)
    base.metadata.create_all(db)
    logging.debug('created DB engine')
    return db


def init_session(db):
    """
    Initialize SQLAlchemy DB session to enable DB operations
    """
    Session = sessionmaker(db)
    logging.debug('created DB session')
    return Session()


def create_message_model(payload: dict):
    """
    Transform dictionary into Message SQLAlchemy Model
    """
    return Message(**payload)


def insert_to_db(message: Message, session: Session):
    """
    Insert Message into DB via session
    """
    session.add(message)
    session.commit()


def init_consumer_client(bootstrap_server: str, topic: str):
    """
    Kafka Consumer client instance retrieves logs from the Kafka
    Producer and allows to iterate over them.
    """
    return KafkaConsumer(
        topic,
        api_version=(2,0,1),
        bootstrap_servers=[bootstrap_server],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group'
    )


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)
    parser = ArgumentParser(description="Consume messangers from Kafka Broker.")
    parser.add_argument("--bootstrap-server", required=True, help="The bootstrap server address the Kafka Producer initially connects to.")
    parser.add_argument("--topic", required=True, type=str, help="The Kafka topic ID.")
    parser.add_argument("--uri", required=True, type=str, help="Database URI.")
    args = parser.parse_args(sys.argv[1:])

    if int(os.environ.get('DEBUG', 0)) == 1:
       # set level of root logger
       logging.getLogger().setLevel(logging.DEBUG)

    # Create Kafka Consumer client instance. It retrieves logs from the Kafka
    # Producer and allows to iterate over them. We then create DB entries
    client = init_consumer_client(args.bootstrap_server, args.topic)
    # Create DB
    db = setup_db(args.uri)
    logging.debug(f"DB URI: {args.uri}")
    # Initialize DB session
    session = init_session(db)
    # iter incoming messages
    for msg in client:
        insert_to_db(create_message_model(msg.value), session)
        logging.debug('db insertion completed')