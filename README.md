# Intro
**Url Uptime Monitoring** monitors a URL for a period of time with a certain frequency. URL, frequency, and period of monitoring are user-defined.

# Architecture
A Kafka Producer periodically collects a payload with the status code, the response elapsed time and the frequency of a user-defined regex pattern. Thereafter, it sends the payload to a Kafka topic via a Kafka Message Broker. The broker forward the received payload to a Kafka Consumer that reads it and store it into the RDBMS.

# Requirements

## Common
* python 3.8
* docker-compose 1.27.4, build 40524192
* kafka-python == 2.0.2
* pytest == 6.2.2

From more info, see https://kafka-python.readthedocs.io/en/master/compatibility.html

## Producer
requests == 2.25.1

## Consumer
psycopg2 == 2.8.5
SQLAlchemy == 1.3.23

# Run
```bash
    URL_TO_TRACK=<http://www.url-to-monitor.com> docker-compose up --build
```
> modify the HOST_IP (KAFKA_ADVERTISED_HOST_NAME) to match your docker host IP

# Tests
Run Unittests

```bash
    python -m pytest <directory>
```

Run DB query
```bash
    
```