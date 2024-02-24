#!/bin/bash

api_url="http://example.com:8000/api/reports"
username=<username>
password=<password>

result=$(curl -s -u "$username:$password" "$api_url")

if [ $? -ne 0 ]; then
    echo "Fehler beim Abrufen der API."
    exit 1
fi

curl -d "$result" http://example.com/restAPI
