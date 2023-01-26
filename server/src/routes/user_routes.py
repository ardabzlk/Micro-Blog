from src.models.user_model import Users

from src.models.models import ResponseModel

from src.services.JWT_service import token_required

# ------------------------------------------------------------
# get all user list


@token_required
def list_users(current_user):
    data = []
    for user in Users.objects():
        data.append(user)
    response = ResponseModel(data)
    return response.get_success_response()
# ------------------------------------------------------------

# ------------------------------------------------------------
# *get user by user id


@token_required
def singleton_user(current_user, uid):

    try:
        user = Users.objects(id=uid).first()
        user = user.to_json()
        data = user
        response = ResponseModel(data)
        return response.get_success_response()
    except:
        response = ResponseModel()
        return response.get_not_found_response()


# ------------------------------------------------------------




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
