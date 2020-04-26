#!/bin/bash

# Set environment variables
export FLASK_APP=stronk
export FLASK_ENV=development
# TODO: Set GOOGLE_APPLICATION_CREDENTIALS to the path that contains your service account private key
export GOOGLE_APPLICATION_CREDENTIALS=""
if [ "$GOOGLE_APPLICATION_CREDENTIALS" != "" ]; then
    flask db upgrade
else
    echo "ERROR: GOOGLE_APPLICATION_CREDENTIALS is not set."
fi

