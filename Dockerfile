FROM python:3.8.3-alpine

RUN useradd -D ave
WORKDIR /home/ave

COPY ./app /home/ubuntu/

WORKDIR /home/ave/app

RUN pip install gunicorn

RUN pip install -r requirements.txt