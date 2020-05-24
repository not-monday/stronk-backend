# Stronk Backend

[![Build Status](https://dev.azure.com/kkjasoncheung/stronk/_apis/build/status/not-monday.stronk-backend?branchName=master)](https://dev.azure.com/kkjasoncheung/stronk/_build/latest?definitionId=1&branchName=master)

This is a [Flask](https://flask.palletsprojects.com/en/1.1.x/blueprints/) backend for Stronk that exposes a [GraphQL](https://graphql.org/) API. We also use [Azure Pipelines](https://azure.microsoft.com/en-us/services/devops/pipelines/) for CI.

# Running with Docker and Docker Compose

## Pre-requisites

Ensure you have [Docker](https://docs.docker.com/install/), [python3](https://www.python.org/downloads/), [pip](https://pip.pypa.io/en/stable/installing/), [postgreSQL](https://www.postgresql.org/) and [newman](https://github.com/postmanlabs/newman) installed.

1. `git clone https://github.com/not-monday/stronk-backend.git`
2. `cd stronk-backend`
3. `source venv/bin/activate` to use venv
4. `pip3 install -r requirements.txt` To install dependencies
5. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
6. Rename the `dotenv` file to `.env` and fill out the secrets.
7. Open `.flaskenv` to fill out any missing environment variables.
8. Ensure you create a database in PostgreSQL that matches the one in `DATABASE_URL` in `.env`. If you don't, follow the instructions below to set up the database!
9. Set up a Firebase Service Account for Stronk if you do not already have one and download the json credentials file
10. Rename the json file to `stronk-google-credentials.json` and copy it to the the root of the project
11. Run `docker-compose up`

Server will be live on port 5000 and database on port 5001.

# Running without Docker and Docker Compose

## Pre-requisites

Ensure you have[python3](https://www.python.org/downloads/), [
](https://pip.pypa.io/en/stable/installing/), [postgreSQL](https://www.postgresql.org/) and [newman](https://github.com/postmanlabs/newman) installed.

1. Set up your virtualenv by following [this guide](https://docs.python.org/3/library/venv.html)
2. `pip install -r requirements.txt`
3. Create a Postgres database. This database will have a database (connect) url in the format `postgresql://{username}:{password}@localhost:{port}/{database name}`
3. Make a copy of `dotenv` and rename it to `.env` and fill in the environment variables. You should also look at `.flaskenv` where you can change `FLASK_ENV`.
4. Set up a Firebase Service Account for Stronk if you do not already have one and download the json credentials file
5. Rename the json file to `stronk-google-credentials.json` and copy it to the the root of the project
6. Run the database migrations `flask db upgrade`
7. Run the server `flask run`

Server will be live on port 5000


# Setting up the database

`docker-compose.yml` will pull the latest version of the official postgres docker image.

Fill in the `DB_NAME` and `DB_PASSWORD` in `.env` which correspond to the `POSTGRES_PASSWORD` and `POSTGRES_DB` in `docker-compose.yml`. Any name is fine for the database, just make sure you remember it so that you can set up the .env file.

A database will be created automatically for you with the name `DB_NAME`. Access from outside the `db` container will require a password whereas access from within does not.

More info on this and the environment variables available [here](https://hub.docker.com/_/postgres).

## Database connection URL

Run this to get which port the container is mapped to `docker ps`

```
DATABASE_URL="postgresql://{username}:{password}@localhost:{port}/{database name}"

# This is mine for example:
# DATABASE_URL="postgresql://postgres:test@localhost:32773/stronk"
```

## Connecting to the database
```
# run this on your host if you need to connect to the database in the container
psql -h localhost -p {port} -U postgres --password
```

## Executing a command 
```
# psql -h localhost -p {port} -U {username} -c "CREATE DATABASE {database name};" --password

# Example:
# psql -h localhost -p 5001 -U postgres  -c "CREATE DATABASE stronk;" --password
#  -c       : lets us run an SQL command directly
```

this is a pretty good [resource](https://docs.docker.com/engine/examples/postgresql_service/) to consult

## Optional

To add mock data to the database so interacting is easier:

```bash
# example:
# psql -h localhost -p 32768 -U postgres -d stronk -a -f ./tests/fixtures/insert_mock_data.sql
psql -h localhost -p {port} -U {user name} -d {database name} -a -f ./tests/fixtures/insert_mock_data.sql
```

# Testing

1. In another terminal, set the environment variable, `TEST_DATABASE_URL` to the address exposed by the `db` service.
2. Run `./scripts/test.sh`

Server will be live on port 5000

- when developing, make sure to run repeat `step 3` to use your virtual env

# Contributing

### [Flask Blueprints](https://flask.palletsprojects.com/en/1.1.x/blueprints/)

We will use Flask Blueprints to modularize the design of the back-end. Blueprints can be found under the `controllers/` directory.
Example usage of blueprints can be found [here](https://flask.palletsprojects.com/en/1.1.x/blueprints/).

### Entry point

The entry point of the backend is `stronk/__init__.py`.
