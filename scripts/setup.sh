#!/bin/bash

# Set environment variables
export FLASK_APP=stronk
export FLASK_ENV=development
flask db upgrade
