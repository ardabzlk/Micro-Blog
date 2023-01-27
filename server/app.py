# imports
import json
from flask import Flask
# This extension adds a toolbar overlay to Flask applications containing useful information for debugging. =>
from src.routes.user_routes import users, singleton_user, user_posts
from src.routes.auth.login_register_routes import login, register
from src.routes.blog_posts_routes import add_post, posts, blog_post_categories, single_post, comment, delete_post, vote
from flask_cors import CORS
from src.models.models import db
from api_constants import mongo_password, mongo_user

import os

config_path = os.environ.get("CONFIG_PATH", "server\config.json")

with open(config_path, 'r') as f:
    config = json.load(f)

app = Flask(config["APP_NAME"])
app.config.update(config)

CORS(app)

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config["TESTING"] = config["TESTING"]
app.config['SECRET_KEY'] = config["SECRET_KEY"]

db.init_app(app)
db.disconnect()

user = mongo_user
password = mongo_password
DB_URI = "mongodb+srv://{}:{}@cluster0.ldccoab.mongodb.net/{}?retryWrites=true&w=majority".format(user,
                                                                                                  password, config["DB_NAME"])
db.connect(host=DB_URI)

# ----------------------------------------------------
# * Login Register routes start

app.add_url_rule("/register", view_func=register,
                 methods=["GET", "POST"])

app.add_url_rule("/login", view_func=login,
                 methods=["GET", "POST"])
# ----------------------------------------------------
# ----------------------------------------------------
# * User routes start
app.add_url_rule("/users", methods=["GET"], view_func=users)

app.add_url_rule("/users/<uid>",
                 methods=["GET"], view_func=singleton_user)
# ----------------------------------------------------
# ----------------------------------------------------
# * Blog Posts routes start
app.add_url_rule("/blog_posts/add", view_func=add_post,
                 methods=["POST"])

app.add_url_rule("/blog_posts", view_func=posts,
                 methods=["GET"])

app.add_url_rule("/blog_posts/<param_post_id>", view_func=single_post,
                 methods=["GET"])
app.add_url_rule("/blog_posts/<post_id>", view_func=delete_post,
                 methods=["DELETE"])

app.add_url_rule("/blog_posts/categories", view_func=blog_post_categories,
                 methods=["GET"])

app.add_url_rule("/comment/<comment_id>", view_func=comment,
                 methods=["GET", "POST", "DELETE", "UPDATE"])

app.add_url_rule("/rate", view_func=vote,
                 methods=["POST"])

app.add_url_rule("/users/<uid>/blog_posts", view_func=user_posts,
                 methods=["GET"])

app.run(host="0.0.0.0", port=8000)
