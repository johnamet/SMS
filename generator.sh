#!/usr/bin/env bash
# Generate a long random string

random_string=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32)
client_id=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32)
client_secret=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32)

sed -i '/^APP_SECRET=/s/.*/APP_SECRET='"$random_string"'/' .env
sed -i '/^CLIENT_ID=/s/.*/CLIENT_ID='"$client_id"'/' .env
sed -i '/^CLIENT_SECRET=/s/.*/CLIENT_SECRET='"$client_secret"'/' .env

echo "New secrets generated and replaced in .env file"