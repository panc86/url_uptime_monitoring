import logging
import os
import re
import time
import json
import requests
from requests import Response
from datetime import datetime
from requests.exceptions import ConnectionError
from kafka import KafkaProducer


# initialize logger
logger = logging.getLogger("producer")


def regex_compiler(regex: str):
    """
    Regex compiler function to transform input argument
    """
    return re.compile(regex, re.IGNORECASE)


def get_status_code(response: Response):
    """
    The status of the response (int)
    """
    return response.status_code if response else None


def get_elapsed_seconds(response: Response):
    """
    Time elapsed from sending the request
    to the arrival of the response (float)
    """
    return response.elapsed.total_seconds() if response else 0


def get_matches_count(text, regex):
    """
    Occurrences count of a regex
    pattern within the url content.
    It might be slow for large text content.
    """
    return len(regex.findall(text)) if regex else 0


def get_response(url: str):
    """
    Return response only if request is successful
    """
    try:
        response = requests.get(url)
    except ConnectionError as e:
        raise SystemExit(e)
    return response


def get_payload(response: Response):
    """
    Return URL payload from response content
    """
    payload = dict()
    payload["created_at"] = datetime.utcnow().isoformat()
    payload["status_code"] = get_status_code(response)
    payload["elapsed_seconds"] = get_elapsed_seconds(response)
    return payload


def tracking(url, topic, client, frequency=5, regex=None):
    """
    Monitor a given URL every with a user-defined frequency in seconds
    and forward response payloads to a Kafka consumer via the Kafka Broker.
    """
    # keep alive
    while True:
        response = get_response(url)
        payload = get_payload(response)
        if regex:
            payload['regex_pattern'] = regex.pattern # reference
            payload['regex_matches'] = get_matches_count(response.text, regex)
        client.send(topic, value=payload)
        logger.debug(f"payload: {payload}")
        time.sleep(frequency)


def init_producer_client(bootstrap_server, api_version=(2,0,1)):
    """
    Initialize Kafka Producer client to connect to the Kafka Broker
    """
    client = KafkaProducer(
        api_version=api_version,
        bootstrap_servers=[bootstrap_server],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    logger.debug(f"is bootstrap_connected: {client.bootstrap_connected()}")
    return client


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    # set default logging level
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)
    # parse arguments
    parser = ArgumentParser(description="Url Uptime Monitoring track a given URL at a user-defined frequency in seconds.")
    parser.add_argument("--url", required=True, help="The URI to monitor.")
    parser.add_argument("--bootstrap-server", required=True, help="The bootstrap server address the Kafka Producer initially connects to.")
    parser.add_argument("--topic", required=True, type=str, help="The Kafka topic ID.")
    parser.add_argument("--frequency", required=False, type=int, default=5, help="Frequency of monitoring in seconds. Default is %(default)s.")
    parser.add_argument(
        "--regex", required=False, type=regex_compiler, help="Regex pattern to search in the response content. Example search: `flood` keyword=`\bfloods?\b`")
    args = parser.parse_args(sys.argv[1:])

    if int(os.environ.get('DEBUG', 0)) == 1:
       # set level of root logger
       logging.getLogger().setLevel(logging.DEBUG)

    # create Kafka Producer client instance
    client = init_producer_client(args.bootstrap_server)

    # start tracking url
    tracking(
        args.url, args.topic, client,
        frequency=args.frequency, regex=args.regex
    )
