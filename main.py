import re
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os, json, boto3, psycopg2
from werkzeug.utils import secure_filename
import requests

UPLOAD_FOLDER = './static/app/images/user_profile_pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
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

    def __init__(self, product_type, country, denomination, year, composition, description, obverse_image_path, reverse_image_path, email):
        self.product_type = product_type
        self.country = country
        self.denomination = denomination
        self.year = year
        self.composition = composition
        self.description = description
        self.obverse_image_path = obverse_image_path
        self.reverse_image_path = reverse_image_path
        self.email = email


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def uploadFile(file):
#     S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
#     file_name = secure_filename(file.filename)
#     new_file_name = session["email"] + "." + file_name.rsplit('.', 1)[1].lower()
#     file_type = "image/" + file_name.rsplit('.', 1)[1].lower()
#     s3 = boto3.client('s3')
#     presigned_post = s3.generate_presigned_post(
#         Bucket = S3_BUCKET_NAME,
#         Key = new_file_name,
#         Fields = {"acl": "public-read", "Content-Type": file_type},
#         Conditions = [
#         {"acl": "public-read"},
#         {"Content-Type": file_type}
#         ],
#         ExpiresIn = 3600
#     )
#     url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET_NAME, new_file_name)
#     #file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
#     r = requests.post(presigned_post['url'], data = presigned_post["fields"])
#     session["profile_picture_path"] = url
#     user = users.query.filter_by(email = session["email"]).first()
#     user.profile_picture_path = session["profile_picture_path"]
#     db.session.commit()

def uploadProfilePicture(file):
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    file_name = secure_filename(file.filename)
    new_file_name = session["email"] + "." + file_name.rsplit('.', 1)[1].lower()
    file_type = "image/" + file_name.rsplit('.', 1)[1].lower()
    s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
    s3.upload_fileobj(file, S3_BUCKET_NAME, "profile_pictures/" + new_file_name, ExtraArgs={'ACL': 'public-read'})
    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET_NAME, "profile_pictures/" + new_file_name)
    session["profile_picture_path"] = url
    user = users.query.filter_by(email = session["email"]).first()
    user.profile_picture_path = session["profile_picture_path"]
    db.session.commit()

def uploadCollectionItem(file):
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    file_name = secure_filename(file.filename)
    new_file_name = session["email"] + "-" + str(session["num_item"]) + "." + file_name.rsplit('.', 1)[1].lower()
    file_type = "image/" + file_name.rsplit('.', 1)[1].lower()
    s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
    s3.upload_fileobj(file, S3_BUCKET_NAME, "collection_items/" + new_file_name, ExtraArgs={'ACL': 'public-read'})
    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET_NAME, "collection_items/" + new_file_name)
    session["num_item"] = session["num_item"] + 1
    user = users.query.filter_by(email = session["email"]).first()
    user.num_item = session["num_item"]
    db.session.commit()
    return url

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route("/")
def start():
    return redirect(url_for("search"))

@app.route("/home/")
def home():
    # items = list(collection_items.query.filter(collection_items.email != session["email"]))
    items = list(collection_items.query.filter(True))
    user_objects = dict()
    for item in items:
        if item.email not in user_objects:
            user = users.query.filter_by(email = item.email).first()
            user_objects[item.email] = user
    if "name" in session:
        return render_template("app/home.html", name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"], is_admin = session["is_admin"], items = items, user_objects = user_objects, logged_in = True)
    else:
        return render_template("app/home.html", name = None, email = None, profile_picture_path = None, is_admin = False, items = items, user_objects = user_objects, logged_in = False)

@app.route("/logout/")
def logout():
    session.pop("name", None)
    session.pop("email", None)
    session.pop("password", None)
    session.pop("profile_picure_path", None)
    session.pop("num_item", None)
    session.pop("is_admin", None)
    session.pop("filling_email", None)
    session.pop("filling_password", None)
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
                session["num_item"] = user.num_item
                session["is_admin"] = user.is_admin
                session["about_me_text"] = user.about_me_text
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
            flash("Passwords don't match")
            add_user = False
        if(add_user):
            session["filling_email"] = f_email
            session["filling_password"] = f_password
            #new_user = users(f_name, f_email, f_password, "app/images/user_profile_pictures/avatar3.png")
            new_user = users(f_name, f_email, f_password, "https://%s.s3.amazonaws.com/%s"%(os.environ.get('S3_BUCKET_NAME'), "profile_pictures/" + "avatar3.png"), 0, False, "Una descripción acerca de mí se encontrará en este lugar pronto...")
            db.session.add(new_user)
            db.session.commit()
            flash("You were signed up successfully")
            return redirect(url_for("login"))
    if "name" in session:
        return redirect(url_for("home"))
    return render_template("authentication/signup.html")

@app.route("/account", methods=["POST", "GET"])
def account():
    flash_messages_view = 1
    if "name" in session:
        if request.method == "POST":
            if request.form.get("change_picture"):
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
                    # filename = secure_filename(file.filename)
                    # new_file_name = session["email"] + "." + filename.rsplit('.', 1)[1].lower()
                    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
                    # flash("Picture changed succesfully.")
                    # session["profile_picture_path"] = "app/images/user_profile_pictures/" + new_file_name
                    # user = users.query.filter_by(email = session["email"]).first()
                    # user.profile_picture_path = session["profile_picture_path"]
                    # db.session.commit()
                    #uploadProfilePicture(file) # This line needs to be uncommented
                    flash("Picture changed successfully.")
                flash_messages_view = 1
            elif request.form.get("change_data"):
                new_name = request.form["name"]
                old_password = request.form["old_password"]
                new_password = request.form["new_password"]
                confirmed_new_password = request.form["confirmed_new_password"]
                current_flag = False
                if(new_name != ""):
                    if(old_password != ""):
                        if(session["password"] == old_password):
                            session["name"] = new_name
                            user = users.query.filter_by(email = session["email"]).first()
                            user.name = session["name"]
                            db.session.commit()
                            flash("Profile name changed successfully")
                        else:
                            flash("Incorrect current password. Please try again.")
                            current_flag = True
                    else:
                        flash("You need to type your current password in order to update your profile name")
                if(new_password != ""):
                    if(confirmed_new_password != ""):
                        if(old_password != ""):
                            if(new_password == confirmed_new_password):
                                if(session["password"] == old_password):
                                    session["password"] = new_password
                                    user = users.query.filter_by(email = session["email"]).first()
                                    user.password = session["password"]
                                    db.session.commit()
                                    flash("Password changed successfully")
                                else:
                                    if(current_flag == False):
                                      flash("Incorrect current password. Please try again.")  
                            else:
                                flash("Passwords don't match")
                        else:
                            flash("You need to type your current password in order to change it")
                    else:
                        flash("You need to retype your password. Please try again.")
                flash_messages_view = 2
        return render_template("app/account.html", name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"], is_admin = session["is_admin"], logged_in = True, flash_messages_view = flash_messages_view)
    else:
        flash("You're not logged in. Please log in or create an acocunt.")
        return redirect(url_for("login"))

@app.route("/add_item", methods=["POST", "GET"])
def add_item():
    if "name" in session:
        if session["is_admin"] == True:
            if request.method == "POST":
                # check if the post request has the file part
                if 'obverse_image' not in request.files:
                    flash('No obverse_image part')
                    return redirect(request.url)
                if 'reverse_image' not in request.files:
                    flash('No reverse_image part')
                    return redirect(request.url)
                obverse_image = request.files['obverse_image']
                reverse_image = request.files['reverse_image']
                # if user does not select file, browser also
                # submit an empty part without filename
                if obverse_image.filename == '':
                    flash('Obverse image not selected')
                    return redirect(request.url)
                if reverse_image.filename == '':
                    flash('Reverse image not selected')
                    return redirect(request.url)
                if obverse_image and reverse_image and allowed_file(obverse_image.filename) and allowed_file(reverse_image.filename):
                    product_type = request.form["type"]
                    country = request.form["country"]
                    denomination = request.form["denomination"]
                    year = request.form["year"]
                    composition = request.form["composition"]
                    description = request.form["description"]
                    # obverse_image_url = uploadCollectionItem(obverse_image) # This line needs to be uncommented
                    # reverse_image_url = uploadCollectionItem(reverse_image) # This line needs to be uncommented
                    obverse_image_url = "fake.com" # This line needs to be commented
                    reverse_image_url = "fake2.com" # This line needs to be commented
                    new_item = collection_items(product_type, country, denomination, year, composition, description, obverse_image_url, reverse_image_url, session["email"])
                    db.session.add(new_item)
                    db.session.commit()
                    flash("Item added successfully")
            items = collection_items.query.filter_by(email = session["email"])
            return render_template("app/add_item.html", name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"], is_admin = session["is_admin"], items = items, logged_in = True)
        else:
            flash("Only admin users can go to this page")
            return redirect(url_for("account"))
    else:
        flash("You're not logged in. Please log in or create an acocunt.")
        return redirect(url_for("login"))

@app.route("/collection", methods=["POST", "GET"])
def collection():
    if "name" in session:
        if session["is_admin"] == True:
            items = collection_items.query.filter_by(email = session["email"])
            return render_template("app/collection.html", name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"], is_admin = session["is_admin"], items = items, logged_in = True)
        else:
            flash("Only admin users can go to this page")
            return redirect(url_for("account"))
    else:
        flash("You're not logged in. Please log in or create an acocunt.")
        return redirect(url_for("login"))

@app.route("/about_me", methods=["POST", "GET"])
def about_me():
    if "name" in session:
        if session["is_admin"] == True:
            return render_template("app/about_me.html",  name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"], is_admin = session["is_admin"], about_me_text = session["about_me_text"], logged_in = True)
        else:
            flash("Only admin users can go to this page")
            return redirect(url_for("account"))
    else:
        flash("You're not logged in. Please log in or create an acocunt.")
        return redirect(url_for("login"))

@app.route("/modify_about_me", methods=["POST", "GET"])
def modify_about_me():
    if "name" in session:
        if session["is_admin"] == True:
            if request.method == "POST":
                new_about_me_text = request.form["modified_description"]
                session["about_me_text"] = new_about_me_text
                user = users.query.filter_by(email = session["email"]).first()
                user.about_me_text = session["about_me_text"]
                db.session.commit()
                return redirect(url_for("about_me"))
            return render_template("app/modify_about_me.html",  name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"], is_admin = session["is_admin"], about_me_text = session["about_me_text"], logged_in = True)
        else:
            flash("Only admin users can go to this page")
            return redirect(url_for("account"))
    else:
        flash("You're not logged in. Please log in or create an acocunt.")
        return redirect(url_for("login")) 

@app.route("/add_collector", methods=["POST", "GET"])
def add_collector():
    if "name" in session:
        if session["is_admin"] == True:
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
                    flash("Passwords don't match")
                    add_user = False
                if(add_user):
                    #new_user = users(f_name, f_email, f_password, "app/images/user_profile_pictures/avatar3.png")
                    new_user = users(f_name, f_email, f_password, "https://%s.s3.amazonaws.com/%s"%(os.environ.get('S3_BUCKET_NAME'), "profile_pictures/" + "avatar3.png"), 0, True, "Una descripción acerca de mí se encontrará en este lugar pronto...")
                    db.session.add(new_user)
                    db.session.commit()
                    flash("User added successfully")
            return render_template("app/add_collector.html", name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"], is_admin = session["is_admin"], logged_in = True)
        else:
            flash("Only admin users can go to this page")
            return redirect(url_for("account"))
    else:
        flash("You're not logged in. Please log in or create an acocunt.")
        return redirect(url_for("login"))

@app.route("/view_collectors", methods=["POST", "GET"])
def view_collectors():
    if request.method == "POST":
        clicked_user  = users.query.filter_by(email = list(request.form.keys())[0]).first()
        session["clicked_user_name"] = clicked_user.name
        session["clicked_user_email"] = clicked_user.email
        session["clicked_user_password"] = clicked_user.password
        session["clicked_user_profile_picture_path"] = clicked_user.profile_picture_path
        session["clicked_user_num_item"] = clicked_user.num_item
        session["clicked_user_is_admin"] = clicked_user.is_admin
        session["clicked_user_about_me_text"] = clicked_user.about_me_text
        return redirect(url_for("about_user"))
    users_objects = list(users.query.filter(True))
    admin_users  = list()
    for usr in users_objects:
        if usr.is_admin == True:
            admin_users.append(usr)
    if "name" in session:
        return render_template("app/view_collectors.html", name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"], is_admin = session["is_admin"], admin_users = admin_users, logged_in = True)
    else:
        return render_template("app/view_collectors.html", name = None, email = None, profile_picture_path = None, is_admin = False, admin_users = admin_users, logged_in = False)

@app.route("/about_user", methods=["POST", "GET"])
def about_user():
    if "name" in session:
        return render_template("app/about_user.html", name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"], is_admin = session["is_admin"], logged_in = True, clicked_user_name = session["clicked_user_name"], clicked_user_email = session["clicked_user_email"], clicked_user_profile_picture_path = session["clicked_user_profile_picture_path"], clicked_user_is_admin = session["clicked_user_is_admin"], clicked_user_about_me_text = session["clicked_user_about_me_text"])
    else:
        return render_template("app/about_user.html", name = None, email = None, profile_picture_path = None, is_admin = False, logged_in = False, clicked_user_name = session["clicked_user_name"], clicked_user_email = session["clicked_user_email"], clicked_user_profile_picture_path = session["clicked_user_profile_picture_path"], clicked_user_is_admin = session["clicked_user_is_admin"], clicked_user_about_me_text = session["clicked_user_about_me_text"])

@app.route("/user_collection", methods=["POST", "GET"])
def user_collection():
    clicked_user_items = collection_items.query.filter_by(email = session["clicked_user_email"])
    if "name" in session:
        return render_template("app/user_collection.html", name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"], is_admin = session["is_admin"], logged_in = True, clicked_user_name = session["clicked_user_name"], clicked_user_email = session["clicked_user_email"], clicked_user_profile_picture_path = session["clicked_user_profile_picture_path"], clicked_user_is_admin = session["clicked_user_is_admin"], clicked_user_about_me_text = session["clicked_user_about_me_text"], clicked_user_items = clicked_user_items)
    else:
        return render_template("app/user_collection.html", name = None, email = None, profile_picture_path = None, is_admin = False, logged_in = False, clicked_user_name = session["clicked_user_name"], clicked_user_email = session["clicked_user_email"], clicked_user_profile_picture_path = session["clicked_user_profile_picture_path"], clicked_user_is_admin = session["clicked_user_is_admin"], clicked_user_about_me_text = session["clicked_user_about_me_text"], clicked_user_items = clicked_user_items)

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        print("Holaaa")
    items = collection_items.query.filter(True)
    country_items = list()
    used = set()
    for item in items:
        if item.country not in used:
            country_items.append(item)
            used.add(item.country)
    if "name" in session:
        return render_template("app/search.html", name = session["name"], email = session["email"], profile_picture_path = session["profile_picture_path"], is_admin = session["is_admin"], logged_in = True, country_items = country_items)
    else:
        return render_template("app/search.html", name = None, email = None, profile_picture_path = None, is_admin = False, logged_in = False, country_items = country_items)

@app.route("/view/users")
def view():
    return render_template("app/users.html", users = users.query.all())