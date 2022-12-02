from flask import Flask, Blueprint, render_template, request, redirect, url_for
from rich import print
from flask_socketio import emit
from threading import Lock
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
            socketio.sleep(10)
            global matches
            matches = _matches
            count += 1
            payload = [{"id":match.id, "status":match.status, 'home':match.ft_score['home'], 'away':match.ft_score['away']} for match in _matches]
            socketio.emit('live_data', {"payload":payload})
            print(f"sent {count}", payload)


wcmu_app = Blueprint("wcmu_app", __name__)

@wcmu_app.route("/")
def index():
    return render_template("index.html", matches=matches, standings=standings, fixtures=fixtures)

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