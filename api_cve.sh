#!/bin/bash

api_url="http://192-46-239-94.ip.linodeusercontent.com:8000/api/reports"
username="dave"
password="MM+mVss1988gz"

result=$(curl -s -u "$username:$password" "$api_url")

if [ $? -ne 0 ]; then
    echo "Fehler beim Abrufen der API."
    exit 1
fi

curl -d "$result" http://192-46-239-94.ip.linodeusercontent.com/restAPI
