import os

from stronk.db.config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

# Create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set up blueprints
from stronk import models, controllers
from stronk.controllers.users import users_page

app.register_blueprint(users_page, url_prefix='/users')

# a simple page that says hello
@app.route('/')
def index():
    return 'Hello, World!'
