FROM python:3.10-slim-buster

WORKDIR /code

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        build-essential \
        nodejs \
        npm \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Install requirements for running tests
COPY ./tools/requirements-test.txt /code/
RUN pip install --no-cache-dir -r requirements-test.txt

RUN npm install -g yarn
RUN npm install -g grunt-cli

COPY . /code/

RUN chmod +x bin/install-static.sh
RUN bin/install-static.sh
# not getting used at this moment
RUN chmod +x bin/wait-for-it.sh

ENV PYTHONUNBUFFERED=1
