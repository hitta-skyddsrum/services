#!/bin/bash

sh  $(dirname $0)/wait-for-database.sh
coverage run --source="$PWD/HittaSkyddsrum" --omit="*/tests/*" -m HittaSkyddsrum/tests/shelters && codecov
