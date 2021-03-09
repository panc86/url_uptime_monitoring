# Intro
**Url Uptime Monitoring** tracks a `URL` with a certain `frequency`. Both URL and frequency are user-defined.

# Architecture
A Kafka Producer periodically collects a Request payload with request timestamp, status code, and elapsed time.
Optionally, a REGEX pattern can be provided at runtime to collect frequency of matches.
Thereafter, it sends the payload to a Kafka topic via a Kafka Message Broker.
The broker forward the received payload to a Kafka Consumer that reads it and store it into the RDBMS.

# Requirements

## Common
* python 3.8
* docker-compose 1.27.4, build 40524192
* kafka-python == 2.0.2
* pytest == 6.2.2

From more info, see https://kafka-python.readthedocs.io/en/master/compatibility.html

## Producer
* requests == 2.25.1

## Consumer
* SQLAlchemy == 1.3.23
* psycopg2 == 2.8.5

# Run
```bash
    URL_TO_TRACK=<http://url-to-track> BROKER_IP=<docker-host-ip> docker-compose up --build
```
> Notes
> For more info on BROKER_IP (i.e. KAFKA_ADVERTISED_HOST_NAME), see [#2](https://github.com/wurstmeister/kafka-docker#pre-requisites)
> * REGEX=`<regex-str>` to enable pattern matching
> * DEBUG=1 to enable service logging

# Tests
Unit tests are implemented in the CI pipeline but can be run locally as follows:

```bash
    pytest
```
> Make sure the environment variables in `.env` are loaded and the services are running

# Next Steps
* Remove hardcoded sensitive variables
* Extend tests coverage
* Better organization of the tests layout
* Add database reading behaviour
* Distribute data over multiple files for scalability
