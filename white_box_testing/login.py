import re
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os, json, boto3, psycopg2
from werkzeug.utils import secure_filename
import requests
import datetime
from sqlalchemy import desc
from utils import convert_uri

# Modifying testing

UPLOAD_FOLDER = './static/app/images/user_profile_pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

global_arg = None
app = Flask(__name__)
app.secret_key = "\xdb\x9d\xc6\x08\xe9\x1d\xaa\x7f\xe5\xd6\xfb\xf7\xcb]\x04\xd4c\x0f\xaf$\x83\xd5\x16\x94"
app.permanent_session_lifetime = timedelta(days=5)
app.config['SQLALCHEMY_DATABASE_URI'] = convert_uri(os.environ['DATABASE_URL'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     'connect_args': {'sslmode':'require'}
# }
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    profile_picture_path = db.Column(db.String(800))
    num_item = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)
    about_me_text = db.Column(db.Text)

    def __init__(self, name, email, password, profile_picture_path, num_item, is_admin, about_me_text):
        self.name = name
        self.email = email
        self.password = password
        self.profile_picture_path = profile_picture_path
        self.num_item = num_item
        self.is_admin = is_admin
        self.about_me_text = about_me_text
        

class collection_items(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    product_type = db.Column(db.String(50))
    country = db.Column(db.String(100))
    denomination = db.Column(db.String(100))
    year = db.Column(db.String(20))
    composition = db.Column(db.String(100))
    description = db.Column(db.String(500))
    obverse_image_path = db.Column(db.String(800))
    reverse_image_path = db.Column(db.String(800))
    email = db.Column(db.String(100))
    is_featured = db.Column(db.Boolean)
    num_views = db.Column(db.Integer)
    date = db.Column(db.Date)

    def __init__(self, product_type, country, denomination, year, composition, description, obverse_image_path, reverse_image_path, email, is_featured, num_views, date):
        self.product_type = product_type
        self.country = country
        self.denomination = denomination
        self.year = year
        self.composition = composition
        self.description = description
        self.obverse_image_path = obverse_image_path
        self.reverse_image_path = reverse_image_path
        self.email = email
        self.is_featured = is_featured
        self.num_views = num_views
        self.date = date

class likes(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    item_id = db.Column(db.Integer)
    user_email = db.Column(db.String(100))

    def __init__(self, item_id, user_email):
        self.item_id = item_id
        self.user_email = user_email

class comments(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    item_id = db.Column(db.Integer)
    user_email = db.Column(db.String(100))
    comment_text = db.Column(db.Text)

    def __init__(self, item_id, user_email, comment_text):
        self.item_id = item_id
        self.user_email = user_email
        self.comment_text = comment_text

db.create_all()

user = users("Elkin", "elkin@gmail.com", "123456", "https://localhost:8080/profile_picure.png", 0, True, "Descripción")
collection_item = collection_items("Billete", "Colombia", "1000 pesos", "2010", "Papel", "", "https://localhost:8080/obverse_image.png", "https://localhost:8080/reverse_image.png", "elkin@gmail.com", True, 0, datetime.date.today())
like = likes(1, "elkin@gmail.com")
comment = comments(1, "elkin@gmail.com", "Comentario..")

@app.route("/login/", methods=["POST", "GET"])
def login():
    email = None
    password = None
    if "filling_email" in session:
        email = session["filling_email"]
    if "filling_password" in session:
        password = session["filling_password"]
    if request.method == "POST":
        f_email = request.form["email"]
        f_password = request.form["password"]
        user = users.query.filter_by(email = f_email).first()
        if(user != None):
            if(f_password == user.password):
                session["filling_email"] = user.email
                session["filling_password"] = user.password
                session["name"] = user.name
                session["email"] = user.email
                session["password"] = user.password
                session["profile_picture_path"] = user.profile_picture_path
                session["num_item"] = user.num_item
                session["is_admin"] = user.is_admin
                session["about_me_text"] = user.about_me_text
                session.permanent = True
                return print('redirect(url_for("home"))')
            else:
               print("Password incorrect. Please try again.") 
        else:
            print("User doesn't exist. Please create an account.")
    if "name" in session:
        print('redirect(url_for("home"))')
    print('return render_template("../authentication/login.html", email = email)')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)