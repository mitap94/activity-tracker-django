FROM python:3
LABEL maintainter="petrovic.m.dimitrije@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

RUN mkdir /src
COPY ./src /src
RUN mkdir /utils
COPY ./utils /utils

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

WORKDIR /src
