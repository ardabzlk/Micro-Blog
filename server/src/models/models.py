from flask_mongoengine import MongoEngine

db = MongoEngine()


class StatusCodeEnums:
    success = {"msg": "Success", "code": 200}
    not_found = {"msg": "Not found", "code": 404}
    bad_request = {"msg": "Bad Request", "code": 400}
    unauthorized = {"msg": "Unauthorized", "code": 401}
    gone = {"msg": "Gone", "code": 410}

# global response model


class ResponseModel:
    def __init__(self, status, msg, data):
        self.status = status
        self.msg = msg
        self.data = data

    def get_response(self):
        return {
            "status": self.status,
            "msg": self.msg,
            "data": self.data
        }
