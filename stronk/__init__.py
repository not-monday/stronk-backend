import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

from stronk.database.config import Config

# Create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Import models to be created
from stronk.models.program import Program
from stronk.models.user import User
from stronk.models.workout import Workout
migrate = Migrate(app, db)

# INITIALLY CREATE DATABASE.
# UNCOMMENT ONLY WHEN RUNNING FOR THE FIRST TIME.
# db.create_all()

# Import blueprints
from stronk import models, controllers
from stronk.controllers.users import users_page
from stronk.controllers.programs import programs_page

# TODO add global error handling for malformed requests
app.register_blueprint(users_page, url_prefix='/users')
app.register_blueprint(programs_page, url_prefix='/programs')

# a simple page that says hello
@app.route('/')
def index():
    return 'Hello, World!'
