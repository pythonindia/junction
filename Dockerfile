FROM python:3.11-bullseye

 

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
ADD . /app
EXPOSE 8000
