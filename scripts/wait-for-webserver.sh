#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until [ $(curl -s -o /dev/null -w "%{http_code}" $host) -ge "404" ]; do
    >&2 echo "Web server  is unavailable - sleeping"
      sleep 1
    done

    >&2 echo "Web server is up - executing command"
    exec $cmd
