#!/usr/bin/env bash
"""a script that starts a flask web application"""
from flask import Flask


app = Flask(__name__)

app.route('/', strict_slashes=False)
def hello_hbnb():
    """ a function that prints hello hbnb at the root"""
    return "Hello HBNB!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')