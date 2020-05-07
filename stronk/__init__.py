from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_graphql import GraphQLView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from graphene import ObjectType, String, Schema

import firebase_admin
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
from stronk.models.workout_exercise_super_sets import WorkoutExerciseSuperSets
from stronk.models.program_workouts import ProgramWorkouts
from stronk.models.program_reviews import ProgramReviews
from stronk.models.weight import Weight
from stronk.schema import schema


migrate = Migrate(app, db, compare_type=True)

# INITIALLY CREATE DATABASE.
# UNCOMMENT ONLY WHEN RUNNING FOR THE FIRST TIME.
# db.create_all()

# Import blueprints
from stronk import models, controllers
from stronk.controllers.programs import programs_page
from stronk.controllers.workouts import workouts_page
from stronk.controllers.exercise import exercise_page

app.register_blueprint(programs_page, url_prefix='/programs')
app.register_blueprint(workouts_page, url_prefix='/workouts')
app.register_blueprint(exercise_page, url_prefix='/exercises')

# Load error handlers
from stronk.errors import handlers as h
from werkzeug.exceptions import HTTPException

app.register_error_handler(HTTPException, h.handle_http_exception)
app.register_error_handler(Exception, h.handle_unexpected_errors)

app.before_request(auth.verify_token)

# a simple page that says hello
@app.route('/')
def index():
    return 'Hello, World!'


""" graphql route
this uses the flask as_view utility which transforms a class to a view function, passing its args to the class constructor
each request will call the class' `dispatch_request()` function

- flask [as_view](https://flask.palletsprojects.com/en/1.1.x/api/#flask.views.View.as_view)
- flask-graphql  [as_view](https://github.com/graphql-python/flask-graphql/blob/master/flask_graphql/graphqlview.py)
"""
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql',
                                                           schema=schema, graphiql=app.debug))

# debug endpoint for graphiql
if (app.debug):
    app.add_url_rule(
        '/graphiql', view_func=GraphQLView.as_view('graphiql', schema=schema, graphiql=True))
