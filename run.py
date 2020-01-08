# USE ONLY FOR DEVELOPMENT
# Runs the development server
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
   return 'Hello, World!'

@app.route('/login/<string:username>')
def login(username):
    return username