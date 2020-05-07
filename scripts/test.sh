#!/bin/bash

# Run unit tests
echo "====== RUNNING UNIT TESTS ====="
python3 -m unittest

# Run GraphQL tests
echo "====== RUNNING GRAPHQL TESTS ====="
python3 tests/graphql_tests.py