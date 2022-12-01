from models.user_model import User
from flask import make_response
from services.JWT_service import token_required

from bson import json_util
import json
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


"""

# 3. Define an user document collection

# Name of the collection by defult the class


# create a user

# user = User(user_id=ObjectId(), name="Salih", surname="Bozlak")
# to save the instance to the mongoDB collection =>
# user.save()


# fetch the user
# user = User.objects(name="Ayşe").first()

# update the user
# user.update(id=rndId)

# # add another user
# user = User(user_id=2, name="Meltem", surname="Bozlak")
# user.save()


# userList = []
# for user in User.objects():
#     userList.append(user.to_json())

# print(userList)
# print(userList)

# fetch all the users
# ----------------------------------------------------
# find users whose  surname-name contains Bozlak
# userList = []
# for user in User.objects(surname__contains="Bozlak"):
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
