FROM python:3
LABEL maintainter="petrovic.m.dimitrije@gmail.com"

ENV PYTHONUNBUFFERED 1 

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN mkdir /src
COPY ./src /src
WORKDIR /src
