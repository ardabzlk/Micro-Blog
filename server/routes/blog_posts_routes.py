from flask import request, make_response
from models.blog_posts_model import blog_posts, blog_categories, blog_post_comment, blog_post_vote
import datetime
from services.Exceptions import InvalidUsage
from services.JWT_service import token_required
from bson import json_util
import json
from models.models import StatusCodeEnums


# ------------------------------------------------------------
# create new post
@token_required
def add_post(current_user):
    # user_id
    # title
    # content
    # date
    # category_id
    # # to save the instance to the mongoDB collection = >
    try:
        json_form_data = request.get_json()
        _user_id = json_form_data.get("user_id")
        _username = json_form_data.get("username")
        _title = json_form_data.get("title")
        _content = json_form_data.get("content")
        _category_id = json_form_data.get("category_id")
        _img_base64 = json_form_data.get("img_base64")
        _date = datetime.datetime.today()
        if (len(_user_id) == 0 or
            len(_title) == 0 or
                len(_content) == 0 or
                _category_id == None):
            return make_response("fields cannot be empty ", StatusCodeEnums)
        else:
            blog_post = blog_posts(author_id=_user_id, title=_title, content=_content,
                                   category_id=_category_id, date=_date, img_base64=_img_base64, author_username=_username)
            blog_post.save()
            return make_response("success ", 200)
    except:
        raise InvalidUsage("This view is gone", status_code=410)
# ------------------------------------------------------------

# ------------------------------------------------------------
# *like


@token_required
def vote(current_user):
    json_body_form_data = request.get_json()
    _post_id = json_body_form_data["post_id"]
    _author_id = json_body_form_data["author_id"]
    _vote_value = json_body_form_data["vote_value"]

    post_exists = blog_post_vote.objects(
        post_id=_post_id, author_id=_author_id).count() > 0
    if post_exists:
        db_vote = blog_post_vote.objects.get(
            post_id=_post_id, author_id=_author_id)

        if (_vote_value == 1 and db_vote.vote_value == 1):
            return make_response("already voted", StatusCodeEnums.stat0["code"])
        elif (_vote_value == 1 and db_vote.vote_value == 2):
            db_vote.update(vote_value=_vote_value)
        elif (_vote_value == 2 and db_vote.vote_value == 2):
            return make_response("already voted", StatusCodeEnums.stat0["code"])
        elif (_vote_value == 2 and db_vote.vote_value == 1):
            db_vote.update(vote_value=_vote_value)
        elif (_vote_value == 0):
            db_vote.update(vote_value=_vote_value)

    else:
        user_vote = blog_post_vote(
            post_id=_post_id, author_id=_author_id, vote_value=_vote_value)
        user_vote.save()

        # json_data_w_backslashes = json_util.dumps(db_vote)
        # json_data = json.loads(json_data_w_backslashes)

    return make_response(StatusCodeEnums.stat0["msg"], StatusCodeEnums.stat0["code"])
    # postun içinde aynı kullanıcının vote varsa güncellenecek yoksa eklenecek

# ------------------------------------------------------------
# ------------------------------------------------------------
# *delete post


@token_required
def delete_post(current_user, post_id):
    if request.method == "DELETE":

        post = blog_posts.objects(id=post_id)
        post.delete()
        return make_response(StatusCodeEnums.stat0["msg"], StatusCodeEnums.stat0["code"])
# ------------------------------------------------------------
# ------------------------------------------------------------
# *add blog category


def add_category():
    # user
    # header
    # content
    # date
    # # to save the instance to the mongoDB collection = >
    try:
        body_form_data = request.get_json()

        blog_post = blog_categories(category_id=body_form_data.get(
            "category_id"), category_name=body_form_data.get("category_name"))
        blog_post.save()
        return make_response("success ", 200)
    except:
        raise InvalidUsage("This view is gone", status_code=410)
# ------------------------------------------------------------

# ------------------------------------------------------------
# *get all posts


@token_required
def posts(current_user):
    posts = []
    for post in blog_posts.objects():
        post["like"] = blog_post_vote.objects(post_id=post.id,
                                              vote_value=1).count()
        post["dislike"] = blog_post_vote.objects(post_id=post.id,
                                                 vote_value=2).count()
        posts.append(post)
    return make_response(posts)
# ------------------------------------------------------------

# ------------------------------------------------------------
# *get blog categories


@token_required
def blog_post_categories(current_user):
    post_categories = []
    for category in blog_categories.objects():
        post_categories.append(category)
    return make_response(post_categories)
# ------------------------------------------------------------

# ------------------------------------------------------------
# *get post details


@token_required
def single_post(current_user, param_post_id):
    response = []
    # try:
    post = blog_posts.objects(id=param_post_id).first()
    post["like"] = blog_post_vote.objects(post_id=param_post_id,
                                          vote_value=1).count()
    post["dislike"] = blog_post_vote.objects(post_id=param_post_id,
                                             vote_value=2).count()
    # post = user.to_json()
    response.append(post)

    return make_response(response, 200)
    # except:
    #     response["data"] = "User not found"
    #     response["status"] = 404
    #     return make_response(response, 404)
# ------------------------------------------------------------


@token_required
def comment(current_user, comment_id):
    response = []
    if request.method == "GET":
        comment = blog_post_comment.objects(post_id=comment_id)
        response.append(comment)
        return make_response(response, StatusCodeEnums.stat0["code"])
    elif request.method == "POST":
        json_body_form_data = request.get_json()
        _post_id = json_body_form_data["post_id"]
        _author_id = json_body_form_data["author_id"]
        _author_username = json_body_form_data["author_username"]
        _date = datetime.datetime.now()
        _comment_content = json_body_form_data["comment_content"]
        if (len(_post_id) == 0 or
                len(_author_id) == 0 or
                len(_comment_content) == 0):
            return make_response(StatusCodeEnums.stat2["msg"], StatusCodeEnums.stat2["code"])
        else:
            new_comment = blog_post_comment(post_id=_post_id, author_id=_author_id,
                                            date=_date, comment_content=_comment_content, author_username=_author_username)
            new_comment.save()
            return make_response(StatusCodeEnums.stat0["msg"], StatusCodeEnums.stat0["code"])
    elif request.method == "DELETE":
        json_body_form_data = request.get_json()
        _comment_id = json_body_form_data["id"]
        post = blog_post_comment.objects(id=_comment_id).first()
        post.delete()
        return make_response(StatusCodeEnums.stat0["msg"], StatusCodeEnums.stat0["code"])
    else:
        return make_response(StatusCodeEnums.stat2["msg"], StatusCodeEnums.stat2["code"])

# ------------------------------------------------------------


# test


def group_test():
    pipeline = [
        {"$group": {"_id": "637a1494401d77d7338bdf9e", }}
    ]
    #
    docs = blog_posts.objects().aggregate(pipeline)
    response = []
    for doc in docs:
        response.append(doc)
    json_data_w_backslashes = json_util.dumps(response)
    json_data = json.loads(json_data_w_backslashes)

    return make_response(json_data)
