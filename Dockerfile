FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./src /app/src
COPY ./.env /app/.env

RUN apk update && \
    apk add --no-cache git && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/*

USER 1000

ENV PYTHONPATH=src