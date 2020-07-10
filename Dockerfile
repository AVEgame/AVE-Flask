FROM python:3.8.3-alpine

RUN apk add libmagic

RUN pip install gunicorn
COPY ./requirements.txt /
RUN pip install -r requirements.txt

RUN adduser --uid 1000 --home /home/ubuntu --disabled-password ubuntu
USER ubuntu
WORKDIR /home/ubuntu
COPY ./app ./app
WORKDIR /home/ubuntu/app

CMD ["/usr/local/bin/gunicorn", "app:app", "-b", "0.0.0.0:8000","-w", "8"]