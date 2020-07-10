FROM python:3.8.3-alpine

COPY ./app ./app
WORKDIR /app

RUN pip install gunicorn

RUN pip install -r requirements.txt