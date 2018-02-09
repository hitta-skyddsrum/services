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

echo "### START /api/v1/shelters"
shelters_url="localhost:5000/api/v1/shelters/" 

echo "When no query params are passed, an accurate error message should be provided"
response=$(curl -s $shelters_url)
message=$(get_json_value "$response" ".message")
assert_equals "$message" "Bad query params"

echo "When retrieving a shelter accurate properties should be given"
response=$(curl -s "${shelters_url}1")
assert_equals "$(get_json_value "$response" ".id")" "1"
assert_equals "$(get_json_value "$response" ".shelterId")" "142784-8"
assert_equals "$(get_json_value "$response" ".goid")" "5559A55A6966B0002070D6A1B801F496"
assert_equals "$(get_json_value "$response" ".address")" "Sockerbruksgatan 3"
assert_equals "$(get_json_value "$response" ".slots")" "80"

echo "When passing lat and long query params, nearby shelters should be given"
response=$(curl -s "${shelters_url}?lat=59.3618&long=18.1205")
assert_equals "$(get_json_array_length "$response")" "10"
assert_equals "$(get_json_value "$response" ".[0].id")" "62682"

echo "### END /api/v1/shelters"
echo ""
echo "### START /api/v2/shelters"
shelters_url="localhost:5000/api/v2/shelters/" 

echo "When retrieving a shelter accurate properties should be given"
response=$(curl -s "${shelters_url}142784-8")
assert_equals "$(get_json_value "$response" ".id")" "1"
assert_equals "$(get_json_value "$response" ".shelterId")" "142784-8"
assert_equals "$(get_json_value "$response" ".goid")" "5559A55A6966B0002070D6A1B801F496"
assert_equals "$(get_json_value "$response" ".address")" "Sockerbruksgatan 3"
assert_equals "$(get_json_value "$response" ".slots")" "80"

echo "When passing lat and long query params, nearby shelters should be given"
response=$(curl -s "${shelters_url}?lat=59.3618&long=18.1205")
assert_equals "$(get_json_array_length "$response")" "10"
assert_equals "$(get_json_value "$response" ".[0].id")" "62682"

echo "When searching for hospitals an array with results should be returned"
response=$(curl -s "${shelters_url}142784-8/hospitals")
assert_equals "$(get_json_value "$response" ".[0].hsaId")" "SE2321000131-E000000003019"

echo "### END /api/v1/shelters"
echo ""
echo "### START /api/v2/shelters"
shelters_url="localhost:5000/api/v2/shelters/" 


if [ "$Errors" -gt "0" ]; then
  exit 1
else
  exit 0
fi
