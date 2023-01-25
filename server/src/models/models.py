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
    def __init__(self, data=None):
        self.data = data

    def get_success_response(self):
        return ({
            "msg": StatusCodeEnums.success["msg"],
            "data": self.data
        }, StatusCodeEnums.success["code"])

    def get_not_found_response(self):
        return ({
            "msg": StatusCodeEnums.not_found["msg"],
        }, StatusCodeEnums.not_found["code"])

    def get_bad_request_response(self):
        return ({
            "msg": StatusCodeEnums.bad_request["msg"],
        }, StatusCodeEnums.bad_request["code"])

    def get_unauthorized_response(self):
        return ({
            "msg": StatusCodeEnums.unauthorized["msg"],
        }, StatusCodeEnums.unauthorized["code"])
