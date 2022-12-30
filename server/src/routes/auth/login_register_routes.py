from flask import request, make_response
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from src.models.user_model import User
from src.services.Exceptions import InvalidUsage
import datetime
import jwt
from bson import json_util
import json

# ------------------------------------------------------------
# create new user


def register():
    # # to save the instance to the mongoDB collection = >
    token = None
    post_data = request.json
    body_form_data = request.get_json()
    user_check = User.objects(email=body_form_data.get('email')).first()
    try:
        if (len(body_form_data["name"]) == 0 or len(body_form_data["surname"]) == 0 or
                len(body_form_data["username"]) == 0 or len(body_form_data["email"]) == 0 or
                len(body_form_data["password"]) == 0):
            return make_response("empty field", 200)
        elif user_check:
            return make_response('User already exists', 401, {'WWW-Authenticate': 'Basic realm="User Exists"'})
        else:
            hash_hassword = generate_password_hash(
                body_form_data.get('password'), method='sha256')
            user = User(name=body_form_data.get('name'),
                        surname=body_form_data.get('surname'), username=body_form_data.get('username'), password=hash_hassword, email=body_form_data.get('email'))
            user.save()
            token = jwt.encode({'email': user.email, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=30)}, 'micro-blog-playground')
            post_data["token"] = token
            response = {"result": post_data, "status": "success",
                        "message": "user created"}
            return make_response(response, 200)
    except:
        raise InvalidUsage('This view is gone', status_code=410)
# ------------------------------------------------------------

# ------------------------------------------------------------
# user login


def login():
    body_form_data = request.get_json()
    authUserEmail = body_form_data.get('email')
    authPassword = body_form_data.get('password')

    if (len(authUserEmail) == 0 or len(authPassword) == 0):
        return make_response("empty field", 200)
    elif not authUserEmail or not authPassword:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    else:
        user = User.objects(email=authUserEmail).first()

        if not user:
            return make_response('No such user', 404, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        else:
            if check_password_hash(user.password, authPassword):
                response_data = {"uid": user.id}
                response_data["username"] = user.username
                token = jwt.encode({'email': user.email, 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(hours=6)}, 'micro-blog-playground')
                response_data["token"] = token

                json_data_with_backslashes = json_util.dumps(response_data)
                json_data = json.loads(json_data_with_backslashes)
                return make_response(json_data, 200)
            else:
                return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


# -----------------------------------------------------------
