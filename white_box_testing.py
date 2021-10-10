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

# def computeLPSArray(pat, M, lps): 
#     len = 0 # length of the previous longest prefix suffix 
  
#     lps[0] # lps[0] is always 0 
#     i = 1
  
#     # the loop calculates lps[i] for i = 1 to M-1 
#     while i < M: 
#         if pat[i]== pat[len]: 
#             len += 1
#             lps[i] = len
#             i += 1
#         else: 
#             # This is tricky. Consider the example. 
#             # AAACAAAA and i = 7. The idea is similar  
#             # to search step. 
#             if len != 0: 
#                 len = lps[len-1] 
  
#                 # Also, note that we do not increment i here 
#             else: 
#                 lps[i] = 0
#                 i += 1

# # Python program for KMP Algorithm 
# def KMPSearch(pat, txt):
#     M = len(pat) 
#     N = len(txt) 
  
#     # create lps[] that will hold the longest prefix suffix  
#     # values for pattern 
#     lps = [0]*M 
#     j = 0 # index for pat[] 
  
#     # Preprocess the pattern (calculate lps[] array) 
#     computeLPSArray(pat, M, lps) 
  
#     i = 0 # index for txt[] 
#     while i < N: 
#         if pat[j] == txt[i]: 
#             i += 1
#             j += 1
  
#         if j == M: 
#             return True
  
#         # mismatch after j matches 
#         elif i < N and pat[j] != txt[i]: 
#             # Do not match lps[0..lps[j-1]] characters, 
#             # they will match anyway 
#             if j != 0: 
#                 j = lps[j-1] 
#             else: 
#                 i += 1
#     return False

# def search_in_database(search_text):
#     ans = list()
#     items = list(collection_items.query.filter(True))
#     key_words = list(map(lambda x: x.lower(), search_text.split()))
#     for item in items:
#         added = False
#         for key_word in key_words:
#             if(key_word == "monedas"):
#                 key_word = "moneda"
#             if(key_word == "billetes"):
#                 key_word = "billete"
#             if(added):
#                 break
#             if(KMPSearch(key_word, item.product_type.lower())):
#                 ans.append(item); added = True
#             elif(KMPSearch(key_word, item.country.lower())):
#                 ans.append(item); added = True
#             elif(KMPSearch(key_word, item.denomination.lower())):
#                 ans.append(item); added = True
#             elif(KMPSearch(key_word, item.year.lower())):
#                 ans.append(item); added = True
#             elif(KMPSearch(key_word, item.composition.lower())):
#                 ans.append(item); added = True
#             elif(KMPSearch(key_word, item.description.lower())):
#                 ans.append(item); added = True
#     return ans

# def get_comments(item_id):
#     response = ""
#     item_comments = comments.query.filter(comments.item_id == item_id)
#     for c in item_comments:
#         user = users.query.filter_by(email = c.user_email).first()
#         response += user.name + "*" + user.profile_picture_path + "*" + c.comment_text + "|"
#     item = collection_items.query.filter(collection_items._id == item_id).first()
#     item.num_views += 1
#     db.session.commit()
#     return response[0:(len(response)-1)]

# Casos de prueba para la función search_in_database
# search_in_database("Billete")
# search_in_database("Monedas y Billetes")
# search_in_database("Bolivia")
# search_in_database("50 centavos")
# search_in_database("2010")
# search_in_database("Acero")
# search_in_database("Kennedy")
# search_in_database("AAA")
# search_in_database("ABAA")

# Casos de prueba para la función get_comments
# get_comments(11)