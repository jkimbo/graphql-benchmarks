FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
ENV PROJECT_ROOT /app
ENV SHELL /bin/bash

RUN mkdir $PROJECT_ROOT

# Install native deps
RUN apt-get update && apt-get install -y build-essential cmake flex bison

COPY requirements.txt $PROJECT_ROOT
RUN pip install -r $PROJECT_ROOT/requirements.txt

WORKDIR $PROJECT_ROOT
COPY . $PROJECT_ROOT

CMD gunicorn server:app --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker --workers=4