FROM python:3.6-alpine

RUN apk --update add vim \
curl \
mariadb-dev \
mariadb-client \
mariadb-dev \
gcc \
gettext \
jq \
libintl \
musl-dev \
git \
sudo \
bash \
wget \
zsh

RUN adduser -D developer
RUN echo "developer ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER developer
WORKDIR /home/developer
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
ENV SHELL=/bin/zsh
ENV PATH=$PATH:/home/developer/.local/bin

COPY --chown=developer . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt --user

ENTRYPOINT ["/bin/zsh", "-c", "while sleep 3600; do :; done"]
