#!/bin/bash

virtualenv $PWD
source bin/activate
# https://github.com/Miserlou/Zappa/issues/1471
pip install pip==9.0.3
pip install -r requirements.txt
envsubst < zappa_settings.json.tpl > zappa_settings.json

if [ $TRAVIS_BRANCH == 'master' ]; then
  echo "Deploying to production"
  zappa update prod || zappa deploy prod
else
  echo "Deploying to $TRAVIS_BRANCH"
  zappa update $TRAVIS_BRANCH || zappa deploy $TRAVIS_BRANCH
fi
