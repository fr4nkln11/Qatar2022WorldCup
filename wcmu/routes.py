from flask import Flask, Blueprint, render_template, request, redirect, url_for, jsonify
from .models import load
import requests

wcmu_app = Blueprint("wcmu_app", __name__)
@wcmu_app.route("/", methods=["GET", "POST"])
def index():
    print("refresh")
    matches = load()
    return render_template("index.html", matches=matches)

count = 0

@wcmu_app.route("/reload_scores", methods=["GET"])
def reload_scores():
    matches = load()
    if request.method == "GET":
        global count
        payload = [{'home':match.ft_score['home'], 'away':match.ft_score['away']} for match in matches]
        #payload = [{'home':count, 'away':count} for match in matches]
        #count += 1
        print(payload)
        return jsonify(payload)