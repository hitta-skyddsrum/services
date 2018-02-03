#!/bin/bash

virtualenv $PWD
source bin/activate

if [ $TRAVIS_BRANCH == 'master' ]; then
  echo "Deploying to production"
  zappa update prod || zappa deploy prod
else
  echo "Deploying to $TRAVIS_BRANCH"
  zappa update $TRAVIS_BRANCH || zappa deploy $TRAVIS_BRANCH
fi
