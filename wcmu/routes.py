from flask import Flask, Blueprint, render_template, request, redirect, url_for
from .models import matches
import requests

wcmu_app = Blueprint("wcmu_app", __name__)

@wcmu_app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", matches=matches)