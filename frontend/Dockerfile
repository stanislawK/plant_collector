FROM node:10.13.0

EXPOSE 8080

ADD . /plantc/frontend
WORKDIR /plantc/frontend

RUN npm install

ENTRYPOINT bash docker-entrypoint.sh
