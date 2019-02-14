#!/bin/bash

port=3306
echo "Waiting for database at $MYSQL_DATABASE_HOST port $port"

tries=0

until nc -z -v $MYSQL_DATABASE_HOST $port; do
    tries=$((tries+1))
    >&2 echo "MySQL  is unavailable - sleeping $tries seconds"
      sleep $tries
      if [ "$tries" -eq 10 ];then
        echo "Failed after $tries tries."
        exit 1
      fi
    done

    >&2 echo "MySQL is up - executing command"
    exit 0
