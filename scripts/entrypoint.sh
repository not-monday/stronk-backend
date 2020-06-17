#!/usr/bin/env bash
flask db upgrade
# add --host=0.0.0.0 flag to accept requests from outside of localhost
flask run --host=0.0.0.0