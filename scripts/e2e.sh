#!/bin/bash

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGSTOP

DIR=$(dirname "$(readlink -f "$0")")

python $DIR/../run.py &
server_pid=$!
sh $DIR/wait-for-webserver.sh localhost:5000 &
waiter_pid=$!
wait $waiter_pid || { kill -9 $server_pid; exit 1; }
sh $DIR/../e2e/shelters.sh
