from dotenv import load_dotenv
from flask import Flask, jsonify, request, g
from stronk.view.graphql_view import CustomGraphQLView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from graphene import ObjectType, String, Schema

import firebase_admin
from tests.constants import TEST_ID
from stronk.database.config import Config, TestConfig
from stronk.utils import auth

# Load environment variables from .env
load_dotenv()

# Create and configure the app
if not firebase_admin._apps:
    default_app = firebase_admin.initialize_app()

app = Flask(__name__, instance_relative_config=True)
if app.config['ENV'] == 'testing':
    app.config.from_object(TestConfig)
else:
    app.config.from_object(Config)

db = SQLAlchemy(app)

# Import models to be created
from stronk.models.program import Program
from stronk.models.user import User
from stronk.models.workout import Workout
from stronk.models.exercise import Exercise
from stronk.models.workout_exercise import WorkoutExercise
from stronk.models.program_workouts import ProgramWorkouts
from stronk.models.program_reviews import ProgramReviews
from stronk.models.weight import Weight
from stronk.schema import schema


migrate = Migrate(app, db, compare_type=True)

# INITIALLY CREATE DATABASE.
# UNCOMMENT ONLY WHEN RUNNING FOR THE FIRST TIME.
# db.create_all()

from stronk import models

# Load error handlers
from stronk.errors import handlers as h
from werkzeug.exceptions import HTTPException

app.register_error_handler(HTTPException, h.handle_http_exception)
app.register_error_handler(Exception, h.handle_unexpected_errors)

# Environment specific settings
if app.config['ENV'] != 'testing':
    app.before_request(auth.verify_token)
else:
    def initialize_test_g():
        """Initialize values of g for testing purposes."""
        g.id = TEST_ID

    app.before_request(initialize_test_g)

""" graphql route
this uses the flask as_view utility which transforms a class to a view function, passing its args to the class constructor
each request will call the class' `dispatch_request()` function

- flask [as_view](https://flask.palletsprojects.com/en/1.1.x/api/#flask.views.View.as_view)
- flask-graphql  [as_view](https://github.com/graphql-python/flask-graphql/blob/master/flask_graphql/graphqlview.py)
"""
app.add_url_rule('/graphql', view_func=CustomGraphQLView.as_view('graphql',
                                                                 schema=schema, graphiql=app.debug))

# debug endpoint for graphiql
if (app.debug):
    app.add_url_rule(
        '/graphiql', view_func=CustomGraphQLView.as_view('graphiql', schema=schema, graphiql=True))
