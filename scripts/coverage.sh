#!/bin/bash

sh  $(dirname $0)/wait-for-database.sh && \
nosetests --all-modules --with-coverage --cover-package=HittaSkyddsrum && codecov
