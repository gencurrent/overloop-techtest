FROM python:3

RUN apt-get update
RUN apt-get install vim

ENV PYTHONUNBUFFERED=1
WORKDIR /django-tech-test
COPY . /django-tech-test/
RUN pip3 install -r requirements.txt
