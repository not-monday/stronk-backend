#!/bin/sh

# Start virtual env
source venv/bin/activate

# Set environment variables
export FLASK_APP=stronk
export FLASK_ENV=development

# Run flask app
flask run