#!/bin/bash

# Set environment variables
export FLASK_APP=stronk
export FLASK_ENV=development
export FLASK_DEBUG=1
flask db upgrade
