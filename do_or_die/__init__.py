from flask import Flask
from flask_pymongo import PyMongo
import json

app = Flask(__name__)
with open("keys.json") as f:
    keys = json.load(f)
    app.config["SECRET_KEY"] = keys["SECRET_KEY"]
    app.config["MONGO_DBNAME"] = keys["MONGO_DBNAME"]
    app.config["MONGO_URI"] = keys["MONGO_URI"]
mongo = PyMongo(app)
users = mongo.db.users
challenges = mongo.db.challenges
comments = mongo.db.comments

from do_or_die import crud_user, crud_challenge, crud_comment, error
