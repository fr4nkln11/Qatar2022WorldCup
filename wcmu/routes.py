from flask import Flask, Blueprint, render_template, request, redirect, url_for
from .models import refresh
import requests

wcmu_app = Blueprint("wcmu_app", __name__)

@wcmu_app.route("/", methods=["GET", "POST"])
def index():
    print("refresh")
    matches = refresh()
    return render_template("index.html", matches=matches)