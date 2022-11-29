from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_socketio import emit
from threading import Lock
import json
from .models import loadMatchData, loadStandingsData, loadFixturesData
from . import socketio
import requests

thread = None
thread_lock = Lock()
initial_load = loadMatchData()
matches = initial_load
standings = loadStandingsData()
fixtures = loadFixturesData()

def background_thread():
    #Example of how to send server generated events to clients.
    count = 0
    while True:
        _matches = loadMatchData()
        socketio.sleep(5)
        global matches
        matches = _matches
        count += 1
        status = json.dumps([match.status for match in _matches])
        scores = [{'home':match.ft_score['home'], 'away':match.ft_score['away']} for match in _matches]
        #scores = [{'home':count, 'away':count} for match in matches]
        socketio.emit('fresh_data', {'scores': scores, 'status': status})
        print("\n" + str(count) + " sent\n" + str(scores) + "\n" + str(status) + "\n")

wcmu_app = Blueprint("wcmu_app", __name__)
@wcmu_app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", matches=matches, standings=standings, fixtures=fixtures)
        
@socketio.on('connect')
def connect():
    print('\nClient connected\n')
    
    if 2 == 2:
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def disconnect():
    print('\nClient disconnected\n\n')