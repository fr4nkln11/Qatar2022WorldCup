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
        if _matches:
            socketio.sleep(1)
            global matches
            matches = _matches
            count += 1
            status = json.dumps([match.status for match in _matches])
            scores = [{'home':match.ft_score['home'], 'away':match.ft_score['away']} for match in _matches]
            #scores = [{'home':count, 'away':count} for match in matches]
            socketio.emit('live_data', {'scores': scores, 'status': status})
            print("\n" + str(count) + " sent\n" + str(scores) + "\n" + str(status) + "\n")

wcmu_app = Blueprint("wcmu_app", __name__)

@wcmu_app.route("/")
def index():
    return render_template("index.html", matches=matches)

@wcmu_app.route("/standings")
def standings_route():
    return render_template("standings.html", standings=standings)

@wcmu_app.route("/fixtures")
def fixtures_route():
    return render_template("fixtures.html", fixtures=fixtures)
        
@socketio.on('connect')
def connect():
    print('\nClient connected\n')
    
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def disconnect():
    print('\nClient disconnected\n\n')