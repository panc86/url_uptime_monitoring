import re
import time
import json
import requests
from kafka import KafkaProducer


def get_status_code(response):
    """
    The status of the response (int)
    """
    return response.status_code


def get_elapsed_seconds(response):
    """
    Time elapsed from sending the request
    to the arrival of the response (float)
    """
    return response.elapsed.total_seconds()


def get_matches_count(response, pattern):
    """
    Occurrences count of a regex
    pattern within the url content.
    It might be slow for large text content.
    """
    return len(re.findall(pattern, response.text.lower())) if pattern else 0


def get_payload(url, pattern):
    """
    Return URL payload if request is successful
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError('Bad URL')
    return dict(
        status_code=get_status_code(response),
        elapsed_seconds=get_elapsed_seconds(response),
        regex_matches=get_matches_count(response, pattern),
        regex_pattern=str(pattern)
    )


t_0 = time.time()
def monitor(url, client, topic=None, pattern=None, frequency=3, deadline=30):
    """
    Monitor a given URL every with a user-defined frequency
    and within a deadline. Both time bounds are in seconds.
    Returns itself recursively until specified deadline is met.
    """
    elapsed = time.time() - t_0
    if elapsed > deadline:
        return
    time.sleep(frequency)
    client.send(topic, value=get_payload(url, pattern=pattern))
    return monitor(url, client, topic, pattern, frequency, deadline)


def main(args):
    from argparse import ArgumentParser
    parser = ArgumentParser(description="WAMS monitor a given URI every --frequency seconds for --deadline seconds.")
    parser.add_argument("--url", required=True, help="The URI to monitor.")
    parser.add_argument("--host", required=False, help="The bootstrap server address the Kafka Producer initially connects to.")
    parser.add_argument("--frequency", required=False, type=int, default=5, help="Frequency of monitoring in seconds. Default is %(default)s.")
    parser.add_argument("--deadline", required=False, type=int, default=500,help="Total period of monitoring in seconds. Default is %(default)s.")
    parser.add_argument("--topic", required=False, type=str, default='test', help="The Kafka topic ID. Default is %(default)s.")
    parser.add_argument(
        "--pattern", required=False, type=str, help="Regex pattern to search in the response content. Example search: `flood` keyword=`\bfloods?\b`")
    args = parser.parse_args(args)

    # Create Kafka Producer client instance
    client = KafkaProducer(
        bootstrap_servers=[args.host], api_version=(2,0,1),
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    print(f"is bootstrap_connected: {client.bootstrap_connected()}")

    # start monitoring
    monitor(
        args.url, client, topic=args.topic, pattern=args.pattern,
        frequency=args.frequency, deadline=args.deadline
    )

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
