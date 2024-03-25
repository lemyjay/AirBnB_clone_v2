#!/usr/bin/python3
'''
A script that starts a Flask web app.
The app must be listening on 0.0.0.0, port 5000
'''
from flask import Flask, render_template
from models import storage
from models.state import State
from datetime import datetime

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    '''Route to lists the states'''
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def teardown_session(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
