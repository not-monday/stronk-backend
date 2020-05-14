#!/bin/bash

# By default, set environment variables for development.
# Use a --test flag to modify the FLASK_ENV for testing.
export FLASK_APP=stronk

# Set appropriate FLASK_ENV
if [[ -n "$1" ]] && [[ "$1" == --testing ]]; then
    echo "Setting up testing environment"
    export FLASK_ENV=testing
else
    echo "Setting up development environment"
    export FLASK_ENV=development
fi

export FLASK_DEBUG=1
export GOOGLE_APPLICATION_CREDENTIALS=stronk-google-credentials.json

# Run DB migrations
flask db upgrade
