FROM python:3.8.3-alpine

RUN apk add libmagic

COPY ./app ./app
WORKDIR /app

RUN pip install gunicorn

RUN pip install -r requirements.txt

CMD ["/usr/local/bin/gunicorn", "app:app", "-b", "0.0.0.0:8000","-w", "8"]