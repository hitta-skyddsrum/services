#!/bin/bash

DIR=$(dirname "$(readlink -f "$0")")

python $DIR/../run.py &
sh $DIR/wait-for-webserver.sh localhost:5000
sh $DIR/../e2e/shelters.sh
