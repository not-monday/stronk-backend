#!/bin/bash

# Set environment variables
export FLASK_APP=stronk
export FLASK_ENV=development
# TODO: Set GOOGLE_APPLICATION_CREDENTIALS to the path that contains your service account private key
export GOOGLE_APPLICATION_CREDENTIALS=""
export GOOGLE_APPLICATION_CREDENTIALS="stronk-df73b-firebase-adminsdk-gg4i5-86127a6e73.json"
if [ "$GOOGLE_APPLICATION_CREDENTIALS" != "" ]; then
    flask db upgrade
else
    echo "ERROR: GOOGLE_APPLICATION_CREDENTIALS is not set."
fi

