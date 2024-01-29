FROM python:3.10-slim

RUN mkdir /fastapp

WORKDIR /fastapp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

