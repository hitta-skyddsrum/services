FROM python:2.7-alpine

RUN apk --update add vim \
mariadb-dev \
mariadb-client \
mariadb-libs \
gcc \
musl-dev \
git

COPY . /usr/src/app

WORKDIR /usr/src/app
RUN pip install pipenv && \
  pipenv install

ENTRYPOINT ["/bin/sh", "-c", "while sleep 3600; do :; done"]
