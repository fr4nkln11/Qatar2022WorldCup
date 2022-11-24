from flask import Flask, Blueprint, render_template, request, redirect, url_for, jsonify
from flask_socketio import emit
from threading import Lock
from .models import load
from . import socketio
import requests

thread = None
thread_lock = Lock()

def background_thread():
    #Example of how to send server generated events to clients.
    count = 0
    while True:
        matches = load()
        socketio.sleep(1.5)
        count += 1
        payload = [{'home':match.ft_score['home'], 'away':match.ft_score['away']} for match in matches]
        #payload = [{'home':count, 'away':count} for match in matches]
        socketio.emit('fresh_data', {'scores': payload})
        print(str(count) + " sent")
        print(payload)

wcmu_app = Blueprint("wcmu_app", __name__)
@wcmu_app.route("/", methods=["GET", "POST"])
def index():
    print("refresh")
    matches = load()
    return render_template("index.html", matches=matches)
        
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')