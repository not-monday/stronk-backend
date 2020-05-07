# Stronk Backend

This is a [Flask](https://flask.palletsprojects.com/en/1.1.x/blueprints/) backend for Stronk.

# Pre-requisites

Ensure you have [python3](https://www.python.org/downloads/), [pip](https://pip.pypa.io/en/stable/installing/) and [postgreSQL](https://www.postgresql.org/) installed.

# Quickstart

1. `git clone https://github.com/not-monday/stronk-backend.git`
2. `cd stronk-backend`
3. `source venv/bin/activate` to use venv
4. `pip3 install -r requirements.txt` To install dependencies
5. Rename the `dotenv` file to `.env` and fill out the secrets
6. Ensure you create a schema in PostgreSQL that matches the one in `DATABASE_URL` in `.env`. If you don't, follow the instructions below to set up the database!
7. Set up a Firebase Service Account for Stronk if you do not already have one and download the json credentials file
8. Rename the json file to `stronk-google-credentials.json` and copy it to the the root of the project
9. `source ./scripts/setup.sh` to run database migrations
10. `flask run` to start server

## OPTIONAL:

To add mock data to the database so interacting is easier:

1.

```bash
# example:
# psql -h localhost -p 32768 -U postgres -d stronk -a -f sql/insert_mock_data.sql
psql -h localhost -p {port} -U {user name} -d {database name} -a -f sql/insert_mock_data.sql
```

Server will be live of port 5000

- when developing, make sure to run repeat `step 2` to use your virtual env

# Setting up the database

## Requirements:

- [Docker](https://docs.docker.com/install/)
- Run `docker pull postgres` to install the latest linux-Arm64 docker image for [postgres](https://hub.docker.com/_/postgres).

## Steps

1. Make sure you're in the root of the project
2. Create an container with the image using this command

```docker
docker run -it --rm --name {image name} -P -d -e POSTGRES_PASSWORD={password} postgres

# example:
# docker run -it --rm --name stronk -P -it -e POSTGRES_PASSWORD=test postgres

# Options:
#  -e       : sets environment variables
#  -P       : publishes ports to host
#  -d       : (can leave out) starts the container in detached mode
#  -it      : allows us to interact (i) with container through stdin/stdout and login through the terminal (t)
# --rm      : cleans up container files on exit
# --name    : gives the container a name
#  -v       : mount the directory supplied to /mnt in the container (modifications are reflected across container and current fs)
```

3. Run this to get which port the container is mapped to `docker ps`
4. Create a database using this command

```
# Any name is fine for the database, just make sure you remember it so that you can set up the .env file
psql -h localhost -p {port} -U {username} -c "CREATE DATABASE {database name};" --password

# example:
# psql -h localhost -p 32773 -U postgres  -c "CREATE DATABASE stronk;" --password
#  -c       : lets us run an SQL command directly
```

5. Set up your .env file

```
DATABASE_URL="postgresql://{username}:{password}@localhost:{port}/{database name}"

# This is mine for example:
# DATABASE_URL="postgresql://postgres:test@localhost:32773/stronk"
```

6. If you need to connect to the database

```
# run this on your host if you need to connect to the database in the container
psql -h localhost -p {port} -U postgres --password
```

this is a pretty good [resource](https://docs.docker.com/engine/examples/postgresql_service/) to consult

# Testing

Set up a test database

1. Fill in `TEST_DATABASE_URL` in your `.env`
2. Run `source scripts/setup.sh --testing`

Run unit tests and graphQL tests

`./test.sh`

# Contributing

### [Flask Blueprints](https://flask.palletsprojects.com/en/1.1.x/blueprints/)

We will use Flask Blueprints to modularize the design of the back-end. Blueprints can be found under the `controllers/` directory.
Example usage of blueprints can be found [here](https://flask.palletsprojects.com/en/1.1.x/blueprints/).

### Entry point

The entry point of the backend is `stronk/__init__.py`.
