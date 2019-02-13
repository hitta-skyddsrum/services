#!/bin/bash

echo "Waiting for database at $MYSQL_DATABASE_HOST"

tries=0

until mysql -h $MYSQL_DATABASE_HOST -u $MYSQL_DATABASE_USER -e "quit"; do
    >&2 echo "MySQL  is unavailable - sleeping"
      sleep 2
      tries=$((tries+1))
      if [ "$tries" -eq 10 ];then
        echo "Failed after $tries tries."
        exit 1
      fi
    done

    >&2 echo "MySQL is up - executing command"
    exit 0
