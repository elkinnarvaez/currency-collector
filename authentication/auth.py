from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")

@auth.route("/login/")
def login():
    return render_template("authentication/login.html")

@auth.route("/signup/")
def signup():
    return render_template("authentication/signup.html")