# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /oTree
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
