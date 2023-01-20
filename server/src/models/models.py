from flask_mongoengine import MongoEngine

db = MongoEngine()


class StatusCodeEnums:
    stat0 = {"msg": "Success", "code": 200}
    stat1 = {"msg": "Not found", "code": 404}
    stat2 = {"msg": "Invalid Request", "code": 400}
    stat3 = {"msg": "Unauthorized", "code": 401}
    stat4 = {"msg": "Something went wrong", "code": 400}

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
