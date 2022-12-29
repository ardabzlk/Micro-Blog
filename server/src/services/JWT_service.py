from functools import wraps
from flask import jsonify, request
import jwt
from src.models.user_model import User
import json


with open('config.json', 'r') as f:
    config = json.load(f)

secret_key = config["SECRET_KEY"]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:

            bearer = request.headers.get(
                'Authorization')    # Bearer YourTokenHere
            token = bearer.split()[1]  # YourTokenHere

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, secret_key,
                              algorithms=['HS256'])
            current_user = User.objects(username=data.get('email')).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated
