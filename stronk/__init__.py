import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
import firebase_admin

from stronk.database.config import Config

# Load environment variables from .env
load_dotenv()

# Create and configure the app
default_app = firebase_admin.initialize_app()
app = Flask(__name__, instance_relative_config=True)
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

migrate = Migrate(app, db)

# INITIALLY CREATE DATABASE.
# UNCOMMENT ONLY WHEN RUNNING FOR THE FIRST TIME.
# db.create_all()

# Import blueprints
from stronk import models, controllers
from stronk.controllers.users import users_page
from stronk.controllers.programs import programs_page
from stronk.controllers.workouts import workouts_page
from stronk.controllers.exercise import exercise_page

# TODO add global error handling for malformed requests
app.register_blueprint(users_page, url_prefix='/users')
app.register_blueprint(programs_page, url_prefix='/programs')
app.register_blueprint(workouts_page, url_prefix='/workouts')
app.register_blueprint(exercise_page, url_prefix='/exercises')

# a simple page that says hello
@app.route('/')
def index():
    return 'Hello, World!'
