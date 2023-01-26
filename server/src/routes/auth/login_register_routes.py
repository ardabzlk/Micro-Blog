from flask import request
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from src.models.user_model import Users
from src.models.models import ResponseModel
import datetime
import jwt
from bson import json_util
import json
import os

# ------------------------------------------------------------
# create new user

config_path = os.environ.get("CONFIG_PATH", "config.json")

with open(config_path, 'r') as f:
    config = json.load(f)

def register():
    # # to save the instance to the mongoDB collection = >
    token = None
    body_form_data = request.get_json()
    user_check = Users.objects(email=body_form_data.get('email')).first()
    try:
        response = ResponseModel()
        if (len(body_form_data["name"]) == 0 or len(body_form_data["surname"]) == 0 or
                len(body_form_data["username"]) == 0 or len(body_form_data["email"]) == 0 or
                len(body_form_data["password"]) == 0):
            return response.get_bad_request_response()
        elif user_check:
            return response.get_bad_request_response()
        else:
            hash_hassword = generate_password_hash(
                body_form_data.get('password'), method='sha256')
            user = Users(name=body_form_data.get('name'),
                        surname=body_form_data.get('surname'), username=body_form_data.get('username'), password=hash_hassword, email=body_form_data.get('email'))
            user.save()
            token = jwt.encode({'email': user.email, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=30)}, config["SECRET_KEY"])
            data = []
            data["token"] = token
            response.data = data
            return response.get_success_response()
    except:
        response = ResponseModel()
        return response.get_bad_request_response()
# ------------------------------------------------------------

# ------------------------------------------------------------
# user login


def login():
    body_form_data = request.get_json()
    authUserEmail = body_form_data.get('email')
    authPassword = body_form_data.get('password')
    response = ResponseModel()
    if (len(authUserEmail) == 0 or len(authPassword) == 0):
        return response.get_bad_request_response()
    elif not authUserEmail or not authPassword:
        return response.get_unauthorized_response()
    else:
        user = Users.objects(email=authUserEmail).first()

        if not user:
            return response.get_not_found_response()
        else:
            if check_password_hash(user.password, authPassword):

                data = {"uid": user.id}
                data["username"] = user.username
                token = jwt.encode({'email': user.email, 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(hours=6)}, config["SECRET_KEY"])
                data["token"] = token

                json_data_with_backslashes = json_util.dumps(data)
                json_data = json.loads(json_data_with_backslashes)
                response.data = json_data
                return response.get_success_response()
            else:
                return response.get_unauthorized_response()


# -----------------------------------------------------------
