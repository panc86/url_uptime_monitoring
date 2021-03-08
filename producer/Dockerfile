FROM python:3.8-alpine
LABEL maintainer='panc86@gmail.com'

WORKDIR /producer
COPY . /producer

# update os, pip and install libraries
RUN set -e; \
    pip install --no-cache-dir -r requirements.txt;

ENTRYPOINT python producer.py --url ${URL} --bootstrap-server ${BOOTSTRAP_SERVER} --topic ${TOPIC_ID} --frequency ${FREQUENCY}
