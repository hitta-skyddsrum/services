#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

until mysql -h $MYSQL_DATABASE_HOST -u $MYSQL_DATABASE_USER -e "quit"; do
    >&2 echo "MySQL  is unavailable - sleeping"
      sleep 1
    done

    >&2 echo "MySQL is up - executing command"
    exec $cmd
