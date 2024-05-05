#!/usr/bin/python3
"""Starts a flask web app"""
import uuid

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    cache_id = uuid.uuid4()
    return render_template('index.html', cache_id=cache_id)


@app.route('/login', strict_slashes=False)
def login():
    cache_id = uuid.uuid4()

    return render_template('pages/login.html', cache_id=cache_id)

if __name__ == '__main__':
    app.run("0.0.0.0", 8081, debug=True)