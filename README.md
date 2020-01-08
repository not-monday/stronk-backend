# Stronk Backend
This is a [Flask](https://flask.palletsprojects.com/en/1.1.x/blueprints/) backend for Stronk.

# Pre-requisites
Ensure you have [python3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/) installed.

# Quickstart
1. `git clone https://github.com/not-monday/stronk-backend.git`
2. `cd stronk-backend`
3. `pip3 install -r requirements.txt` To install dependencies.
3. `./start_dev.sh`

Server will be live of port 5000

# Contributing
### [Flask Blueprints](https://flask.palletsprojects.com/en/1.1.x/blueprints/)
We will use Flask Blueprints to modularize the design of the back-end. Blueprints can be found under the `controllers/` directory.
Example usage of blueprints can be found [here](https://flask.palletsprojects.com/en/1.1.x/blueprints/).

### Entry point
The entry point of the backend is `stronk/__init__.py`.
