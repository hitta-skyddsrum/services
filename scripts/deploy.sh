#!/bin/bash

# https://github.com/Miserlou/Zappa/issues/1471
pip install pip==9.0.3
pip install -r requirements.txt --user
# Waiting for https://github.com/Miserlou/Zappa/pull/1781
pip install https://github.com/kontrollanten/Zappa/archive/kontrollanten-fix-762.zip
# Add python bin to $PATH to enable zappa cmd
python -m site &> /dev/null && PATH="$PATH:`python -m site --user-base`/bin"

if [ $CIRCLE_BRANCH == "master" ]; then
  export ZAPPA_STAGE="prod"
  export ZAPPA_DOMAIN="api.hittaskyddsrum.se"
else
  export ZAPPA_STAGE="${CIRCLE_BRANCH//[^a-zA-Z0-9_]/_}"
  export ZAPPA_DOMAIN="${CIRCLE_BRANCH//[^a-zA-Z0-9]/-}.stageapi.hittaskyddsrum.se"
fi

envsubst < zappa_settings.json.tpl > zappa_settings.json

if zappa status $ZAPPA_STAGE; then
  echo "Updating $ZAPPA_STAGE"
  zappa update $ZAPPA_STAGE
else
  echo "Deploying to $ZAPPA_STAGE"
  zappa deploy $ZAPPA_STAGE && zappa certify -y $ZAPPA_STAGE
fi
