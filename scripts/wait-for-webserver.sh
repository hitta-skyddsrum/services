#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until curl -f $host; do
    >&2 echo "Web server  is unavailable - sleeping"
      sleep 1
    done

    >&2 echo "Web server is up - executing command"
    exec $cmd
