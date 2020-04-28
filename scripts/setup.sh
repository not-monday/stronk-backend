#!/bin/bash

# Set environment variables
export FLASK_APP=stronk
export FLASK_ENV=development
export FLASK_DEBUG=1
export GOOGLE_APPLICATION_CREDENTIALS=stronk-google-credentials.json

flask db upgrade
