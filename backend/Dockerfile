FROM ubuntu:16.04

EXPOSE 5000

RUN apt-get update -y && apt-get install -y python3-pip libpq-dev && apt-get autoremove

RUN pip3 install --upgrade pip

ADD . /plantc/backend
WORKDIR /plantc/backend

RUN pip3 install -e .
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT bash docker-entrypoint.sh
