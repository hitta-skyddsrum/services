#!/bin/bash
Errors=0

Green='\033[0;32m'
Red='\033[0;31m'
Color_Off='\033[0m'

Check_Mark='\xE2\x9C\x94'

assert_equals () {
  if [ "$1" = "$2" ]; then
    echo -e "$Green $Check_Mark Success $Color_Off"
  else
    echo -e "$Red Failed $Color_Off"
    echo -e "$Red Expected $1 to equal $2 $Color_Off"
    Errors=$((Errors  + 1))
  fi
}

get_json_value () {
  echo $1 | jq -r $2
}

get_json_array_length () {
  echo $1 | jq ". | length"
}

echo "### START /api/v2/shelters"
shelters_url="localhost:5000/api/v2/shelters/" 

echo "When retrieving a shelter accurate properties should be given"
response=$(curl -s "${shelters_url}142784-8")
assert_equals "$(get_json_value "$response" ".shelterId")" "142784-8"
assert_equals "$(get_json_value "$response" ".address")" "Sockerbruksgatan 3"
assert_equals "$(get_json_value "$response" ".slots")" "80"

echo "When passing lat and long query params, nearby shelters should be given"
response=$(curl -s "${shelters_url}?lat=59.3618&long=18.1205")
assert_equals "$(get_json_array_length "$response")" "20"
assert_equals "$(get_json_value "$response" ".[0].shelterId")" "163753-5"

echo "### END /api/v2/shelters"

echo "### START /api/v3/shelters"
shelters_url="localhost:5000/api/v3/shelters/" 

echo "When retrieving shelters within a bbox, accurate shelters should be given"
response=$(curl -s "${shelters_url}?bbox=17.939901351928714,59.28355331123377,17.972860336303714,59.305992725442266")
assert_equals "$(get_json_value "$response" ".[0].shelterId")" "125500-7"
assert_equals "$(get_json_value "$response" ".[0].address")" "Vita Liljans Väg 36"
assert_equals "$(get_json_value "$response" ".[0].city")" "Stockholm"
assert_equals "$(get_json_value "$response" ".[0].estateId")" "Coldinuorden 3"
assert_equals "$(get_json_value "$response" ".[0].filterType")" "Sandfilter"
assert_equals "$(get_json_value "$response" ".[0].municipality")" "Stockholm"
assert_equals "$(get_json_value "$response" ".[0].slots")" "150"

echo "### END /api/v3/shelters"

if [ "$Errors" -gt "0" ]; then
  exit 1
else
  exit 0
fi
