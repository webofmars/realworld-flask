#!/usr/bin/env bash

# Run API tests using Postman collection (from https://github.com/gothinkster/realworld/tree/main/api)
# APIURL=http://localhost:3000/api ./run-api-tests.sh

set -x

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

APIURL=${APIURL:-https://api.realworld.io/api}
USERNAME=${USERNAME:-u`date +%s`}
EMAIL=${EMAIL:-$USERNAME@mail.com}
PASSWORD=${PASSWORD:-password}

npx newman run $SCRIPTDIR/Conduit.postman_collection.json \
  --delay-request 500 \
  --global-var "APIURL=$APIURL" \
  --global-var "USERNAME=$USERNAME" \
  --global-var "EMAIL=$EMAIL" \
  --global-var "PASSWORD=$PASSWORD" \
  "$@"
