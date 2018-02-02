FROM python:2.7-alpine

RUN apk --update add vim \
curl \
mariadb-dev \
mariadb-client \
mariadb-libs \
gcc \
musl-dev \
git \
sudo \
bash \
wget \
zsh
RUN pip install pipenv \
zappa 

RUN adduser -D developer
USER developer
WORKDIR /home/developer
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
ENV SHELL=/bin/zsh

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pipenv install

ENTRYPOINT ["/bin/zsh", "-c", "while sleep 3600; do :; done"]
