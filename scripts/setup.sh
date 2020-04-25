#!/bin/sh

# Set environment variables
export FLASK_APP=stronk
export FLASK_ENV=development

# Run flask database migrations
flask db upgrade