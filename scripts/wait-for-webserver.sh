#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

tries=0

until [ $(curl -s -o /dev/null -w "%{http_code}" $host) -ge "404" ]; do
    tries=$((tries+1))
    >&2 echo "Web server is unavailable - sleeping for $tries seconds."
      sleep $tries
      if [ "$tries" -eq 10 ];then
        echo "Failed after $tries tries."
        exit 1
      fi
    done

    >&2 echo "Web server is up"
    exit 0
