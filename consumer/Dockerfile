FROM python:3.8-alpine
LABEL maintainer='panc86@gmail.com'

WORKDIR /consumer
COPY . /consumer

# update os, pip and install libraries
RUN set -e; \
    apk update; \
    apk --no-cache add postgresql-dev gcc python3-dev musl-dev; \
    pip install --no-cache-dir -r requirements.txt;

ENTRYPOINT [ "python", "consumer.py" ]
