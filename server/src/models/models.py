from flask_mongoengine import MongoEngine

db = MongoEngine()

"""
    MongoEngine converts class names to collection names by converting the class name from CamelCase to snake_case.
    For example, the class name BlogPost will be converted to the collection name blog_posts.
    If you want to override this behavior, you can specify a custom collection name by setting the meta attribute on the class.
    For example, the following class will be stored in the collection named blog_posts:
    class BlogPost(db.Document):
        title = db.StringField()
        content = db.StringField()
        meta = {'collection': 'blog_posts'}

"""


class StatusCodeEnums:
    success = {"msg": "Success", "code": 200}
    not_found = {"msg": "Not found", "code": 404}
    bad_request = {"msg": "Bad Request", "code": 400}
    unauthorized = {"msg": "Unauthorized", "code": 401}
    gone = {"msg": "Gone", "code": 410}


# ----------------------------------------------------
"""
    global response model
    @param data: data to be returned
    @return: a response with a specific status code (SatusCodeEnums) and a message
"""


class ResponseModel:
    def __init__(self, data=None):
        self.data = data

    # only this response will return data with success message and 200 status code
    def get_success_response(self):
        return ({
            "msg": StatusCodeEnums.success["msg"],
            "data": self.data
        }, StatusCodeEnums.success["code"])

    def get_not_found_response(self):
        # return a not found response with "not found" message and 404 status code
        return ({
            "msg": StatusCodeEnums.not_found["msg"],
        }, StatusCodeEnums.not_found["code"])

    def get_bad_request_response(self):
        # return a bad request response with "bad request" message and 400 status code
        return ({
            "msg": StatusCodeEnums.bad_request["msg"],
        }, StatusCodeEnums.bad_request["code"])

    def get_unauthorized_response(self):
        # return a unauthorized response with "unauthorized" message and 401 status code
        return ({
            "msg": StatusCodeEnums.unauthorized["msg"],
        }, StatusCodeEnums.unauthorized["code"])
