"""
Path: src/infrastructure/flask/flaskk_app.py
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    "A simple route to test the Flask app."
    return 'Hello from Flask!'
