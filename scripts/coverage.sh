#!/bin/bash

coverage run --source="$PWD/HittaSkyddsrum" --omit="*/tests/*" -m HittaSkyddsrum/tests/shelters && codecov
