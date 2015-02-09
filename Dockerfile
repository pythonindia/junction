FROM ubuntu:14.04
MAINTAINER Anuvrat Parashar "anuvrat@anuvrat.in"

RUN apt-get update && apt-get -y upgrade && apt-get install -y git python2.7 python-pip python-dev postgresql-server-dev-all
ADD requirements.txt /srv/requirements.txt
ADD requirements-dev.txt /srv/requirements-dev.txt
WORKDIR /srv/
RUN pip install -r /srv/requirements.txt
RUN rm -rf /usr/local/lib/python2.7/dist-packages/requests
RUN pip install -r /srv/requirements-dev.txt

