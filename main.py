from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
import psycopg2

UPLOAD_FOLDER = './static/app/images/user_profile_pictures'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    profile_picture_path = db.Column(db.String(200))

    def __init__(self, name, email, password, profile_picture_path):
        self.name = name
        self.email = email
        self.password = password
        self.profile_picture_path = profile_picture_path

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route("/")
def start():
    return redirect(url_for("login"))

@app.route("/home/")
def home():
    if "name" in session:
        return render_template("app/home.html", name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"])
    else:
        flash("You're not logged in. Please type your email and password or create a new account.")
        return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    session.pop("name", None)
    session.pop("email", None)
    session.pop("password", None)
    session.pop("profile_picure_path", None)
    return redirect(url_for("login"))

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
                return redirect(url_for("home"))
            else:
               flash("Password incorrect. Please try again.") 
        else:
            flash("User doesn't exist. Please create an account.")
    if "name" in session:
        return redirect(url_for("home"))
    return render_template("authentication/login.html", email = email)

@app.route("/signup/", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        f_name = request.form["name"]
        f_email = request.form["email"]
        f_password = request.form["password"]
        f_confirmed_password = request.form["confirmed_password"]
        user = users.query.filter_by(email = f_email).first()
        add_user = True
        if user != None:
            flash("User already exists. Try using a different email.")
            add_user = False
        if(f_password != f_confirmed_password):
            flash("Passwords don't match.")
            add_user = False
        if(add_user):
            session["filling_email"] = f_email
            session["filling_password"] = f_password
            new_user = users(f_name, f_email, f_password, "app/images/user_profile_pictures/avatar3.png")
            db.session.add(new_user)
            db.session.commit()
            print("You were signed up successfully.")
            flash("You were signed up successfully.")
            return redirect(url_for("login"))
    if "name" in session:
        return redirect(url_for("home"))
    return render_template("authentication/signup.html")

@app.route("/account", methods=["POST", "GET"])
def account():
    if "name" in session:
        if request.method == "POST":
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                new_file_name = session["email"] + "." + filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
                flash("Picture changed succesfully.")
                session["profile_picture_path"] = "app/images/user_profile_pictures/" + new_file_name
                user = users.query.filter_by(email = session["email"]).first()
                user.profile_picture_path = session["profile_picture_path"]
                db.session.commit()
        return render_template("app/account.html", name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"])
    else:
        flash("You're not logged in. Please type your email and password or create a new account.")
        return redirect(url_for("login"))

@app.route("/view/users")
def view():
    return render_template("app/view.html", users = users.query.all())