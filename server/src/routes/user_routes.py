from src.models.blog_posts_model import Blog_posts
from src.models.models import StatusCodeEnums
from src.models.user_model import User
from flask import make_response, request
from src.services.JWT_service import token_required

# ------------------------------------------------------------
# get all user list


@token_required
def users(current_user):
    userList = []
    for user in User.objects():
        userList.append(user)
    return make_response(userList)
# ------------------------------------------------------------

# ------------------------------------------------------------
# get all user list


@token_required
def singleton_user(current_user, uid):
    response = {}
    try:
        user = User.objects(id=uid).first()
        user = user.to_json()
        response["data"] = user
        response["status"] = 200

        return make_response(response)
    except:
        response["data"] = "User not found"
        response["status"] = 404
        return make_response(response, 404)


# ------------------------------------------------------------


# *get user posts by user id

@token_required
def user_posts(current_user, uid):
    response = {}
    if request.method == "GET":
        try:
            posts = Blog_posts.objects(author_id=uid)
            response["data"] = posts
            response["status"] = StatusCodeEnums.success["code"]
            response["msg"] = StatusCodeEnums.success["msg"]
            return make_response(response)
        except:
            response["data"] = "User not found"
            response["status"] = StatusCodeEnums.not_found["code"]
            response["msg"] = StatusCodeEnums.not_found["msg"]
            return make_response(response)


"""

# 3. Define an user document collection

# Name of the collection by defult the class


# create a user

# user = User(user_id=ObjectId(), name="john", surname="doe")
# to save the instance to the mongoDB collection =>
# user.save()


# fetch the user
# user = User.objects(name="John").first()

# update the user
# user.update(id=rndId)

# # add another user
# user = User(user_id=2, name="foo", surname="bar")
# user.save()


# userList = []
# for user in User.objects():
#     userList.append(user.to_json())

# print(userList)
# print(userList)

# fetch all the users
# ----------------------------------------------------
# find users whose  surname-name contains doe
# userList = []
# for user in User.objects(surname__contains="doe"):
#     userList.append(user.to_json())
# print(userList)
# ----------------------------------------------------

# ----------------------------------------------------
# how many user are in the collection
# print(User.objects.count())

# order by name field
# userList = []
# for user in User.objects().order_by("surname"):
#     userList.append(user.to_json())
# print(userList)
# ----------------------------------------------------

# ----------------------------------------------------
# delete a user
# user = User.objects(user_id="63778bf2cc442201ca21a45a").first()

# user.delete()

# print(User.objects.count())
# ----------------------------------------------------

# ----------------------------------------------------
# delete all users
# for user in User.objects():
#     user.delete()
# print(User.objects.count())
# ----------------------------------------------------
"""
