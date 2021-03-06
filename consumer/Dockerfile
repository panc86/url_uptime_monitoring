FROM python:3.8-alpine
LABEL maintainer='panc86@gmail.com'

WORKDIR /consumer
COPY . /consumer

# update os, pip and install libraries
RUN set -e; \
    apk -U --no-cache upgrade; \
    apk add --no-cache gcc libc-dev linux-headers; \
    pip install --upgrade pip; \
    pip install --no-cache-dir kafka-python==2.0.2;
