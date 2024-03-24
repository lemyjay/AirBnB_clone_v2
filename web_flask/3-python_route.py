#!/usr/bin/python3
'''
A script that starts a Flask web app.
The app must be listening on 0.0.0.0, port 5000
'''
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Route that displays 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Route that displays just 'HBNB'"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Route that display “C ” followed by the value of the text variable
    (replaces underscore _ symbols with a space )
    """
    if text:
        text = text.replace('_', ' ')

    return "C " + text


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """Route that display “Python ” followed by the value of the text variable
    (replaces underscore _ symbols with a space )
    """
    if text:
        text = text.replace('_', ' ')

    return "Python " + text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
