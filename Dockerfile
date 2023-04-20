FROM python:3.10-slim-buster

WORKDIR /code

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Install requirements for running tests
COPY ./tools/requirements-test.txt /code/
RUN pip install --no-cache-dir -r requirements-test.txt

COPY . /code/
# not getting used at this moment
RUN chmod +x bin/wait-for-it.sh

ENV PYTHONUNBUFFERED=1

EXPOSE 8888
