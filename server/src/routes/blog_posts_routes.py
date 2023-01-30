from flask import request, make_response
from src.models.blog_posts_model import BlogPosts, BlogCategories, BlogPostComments, BlogPostVotes
import datetime
from src.services.JWT_service import token_required
from src.models.models import ResponseModel

"""
def ExampleCRUDMethod():
    if request.method == "POST":
        # response model should be initialized at the beginning of the statement
        response = ResponseModel()
        if request_is_successfull:
            data = "succesfully added"
            # data should be added to the response model before returning it
            response.data = data
            # return the response model with the success message and 200 status code
            return response.get_success_response()
        else:
            # return the response model with the bad request message and 400 status code
            return response.get_bad_request_response()
    
    elif request.method == "GET":
        response = ResponseModel()
        if request_is_successfull:
            data = db.objects().all()
            response.data = data
            return response.get_success_response()

"""

# ------------------------------------------------------------
# */blog_posts/<param_post_id>


@token_required
def post_management(current_user, param_post_id):
    """
    Manage single post
    endpoint: /blog-posts/<param_post_id>

    This method allows to manage a single post
    it can be used to get, update or delete a single post
    it checks if the user is the author of the post before updating or deleting it-
    by comparing the current user id with the author id
    
    *GET
    *PUT
    *DELETE
    
    args: param_post_id
    
    return: response model according to result

    """

    try:
        # add new blog post
        # get single post
        # *GET
        if request.method == "GET":
            data = []
            blog_post = BlogPosts.objects(id=param_post_id).first()
            data.append(blog_post)
            response = ResponseModel(data)
            if (blog_post):
                return response.get_success_response()
            else:
                response = ResponseModel()
                return response.get_not_found_response()

        # update post
        # *PUT
        elif request.method == "PUT":
            blog_post = BlogPosts.objects(id=param_post_id).first()
            response = ResponseModel()
            if current_user.id != blog_post.author_id:
                return response.get_unauthorized_response()
            else:
                json_form_data = request.get_json()
                _title = json_form_data.get("title")
                _content = json_form_data.get("content")
                _category_id = json_form_data.get("category_id")
                _img_base64 = json_form_data.get("img_base64")
                _date = datetime.datetime.today()
                if len(_title) == 0 or len(_content) == 0 or _category_id == None:
                    return response.get_bad_request_response()
                else:
                    blog_post.update(title=_title, content=_content,
                                     category_id=_category_id, date=_date, img_base64=_img_base64)
                    data = []
                    data.append(blog_post)
                    response.data = data
                    return response.get_success_response()

        # delete post
        # *DELETE
        elif request.method == "DELETE":
            blog_post = BlogPosts.objects(id=param_post_id).first()
            response = ResponseModel()

            if current_user.id != blog_post.author_id:
                return response.get_unauthorized_response()
            else:
                blog_post.delete()
                data = ["deleted successfully"]
                data.append(blog_post)
                response.data = data
                return response.get_success_response()

    except:
        response = ResponseModel()
        return response.get_bad_request_response()
# ------------------------------------------------------------
# */blog_posts


@token_required
def posts(current_user):
    """
    Manage all posts
    endpoint: /blog-posts
    
    This method allows to manage all posts
    it can be used to get all posts or add a new post

    *POST
    *GET

    args: none

    return: response model according to result

    """
    # *POST
    # add new blog post
    if request.method == "POST":
        response = ResponseModel()
        json_form_data = request.get_json()
        _user_id = json_form_data.get("user_id")
        _username = json_form_data.get("username")
        _title = json_form_data.get("title")
        _content = json_form_data.get("content")
        _category_id = json_form_data.get("category_id")
        _img_base64 = json_form_data.get("img_base64")
        _date = datetime.datetime.today()
        if len(_user_id) == 0 or len(_title) == 0 or len(_content) == 0 or len(_username) == 0 or _category_id == None:
            return response.get_bad_request_response()
        else:
            blog_post = BlogPosts(author_id=_user_id, title=_title, content=_content,
                                  category_id=_category_id, date=_date, img_base64=_img_base64, author_username=_username)
            blog_post.save()
            data = []
            data.append(blog_post)
            response.data = data
            return response.get_success_response()
    # *GET
    # get all posts
    elif request.method == "GET":
        response = ResponseModel()
        data = []
        for blog_post in BlogPosts.objects():
            blog_post["like"] = BlogPostVotes.objects(post_id=blog_post.id,
                                                      vote_value=1).count()
            blog_post["dislike"] = BlogPostVotes.objects(post_id=blog_post.id,
                                                         vote_value=2).count()
            data.append(blog_post)

        response.data = data
        return response.get_success_response()
# ------------------------------------------------------------
# *like

# *dislike


@token_required
def vote(current_user):
    """
    Vote for a post
    endpoint: /vote

    This method allows to vote for a post
    it can be used to like or dislike a post
    it checks if the user has already voted for the post before
    if the user has already voted for the post, it updates the vote
    if the user has not voted for the post, it adds a new vote

    *POST

    args: none

    return: response model according to result

    """


    response = ResponseModel()
    json_body_form_data = request.get_json()
    _post_id = json_body_form_data["post_id"]
    _author_id = json_body_form_data["author_id"]
    _vote_value = json_body_form_data["vote_value"]

    blog_post = BlogPosts.objects(id=_post_id).first()
    post_vote_exists = BlogPostVotes.objects(
        post_id=_post_id, author_id=_author_id).count() > 0
    if post_vote_exists:
        db_vote = BlogPostVotes.objects.get(
            post_id=_post_id, author_id=_author_id)
        # 1 like
        _like = blog_post.like
        _dislike = blog_post.dislike
        if (_vote_value == 1 and db_vote.vote_value == 1):
            db_vote.delete()
            if _like > 0:
                blog_post.update(like=_like - 1)
                response.data = "vote deleted"
            return response.get_success_response()
        elif (_vote_value == 1 and db_vote.vote_value == 2):
            blog_post.update(like=_like+1, dislike=_dislike-1)
            db_vote.update(vote_value=_vote_value)
            response.data = "vote updated"
            return response.get_success_response()
        elif (_vote_value == 2 and db_vote.vote_value == 2):
            db_vote.delete()
            if _dislike > 0:
                blog_post.update(dislike=_dislike-1)
            response.data = "vote deleted"
            return response.get_success_response()
        elif (_vote_value == 2 and db_vote.vote_value == 1):
            blog_post.update(like=_like-1, dislike=_dislike+1)
            db_vote.update(vote_value=_vote_value)
            response.data = "vote updated"
            return response.get_success_response()
        else:
            return response.get_bad_request_response()
    else:
        user_vote = BlogPostVotes(
            post_id=_post_id, author_id=_author_id, vote_value=_vote_value)
        user_vote.save()
        if (_vote_value == 1):
            blog_post.update(like=+1)
        elif (_vote_value == 2):
            blog_post.update(dislike=+1)

        response.data = user_vote
        return response.get_success_response()


# ------------------------------------------------------------

# ------------------------------------------------------------
# *add blog category


def add_category():
    """
    # ! Deprecated
    Temporary function to add blog categories
    it doesnt have endpoint 
    category_id = StringField(required=True)
    category_name = StringField(required=True)
    """
    try:
        body_form_data = request.get_json()

        blog_post_category = BlogCategories(category_id=body_form_data.get(
            "category_id"), category_name=body_form_data.get("category_name"))
        blog_post_category.save()
        data = []
        data.append(blog_post_category)
        response = ResponseModel(data)
        return response.get_success_response()

    except:
        response = ResponseModel()
        return response.get_bad_request_response()

# ------------------------------------------------------------


# ------------------------------------------------------------
# *get blog categories


@token_required
def blog_post_categories(current_user):
    """
    # ! Deprecated
    get all blog categories
    endpoint: -
    """
    data = []
    for category in BlogCategories.objects():
        data.append(category)
    response = ResponseModel(data)
    return response.get_success_response()


# ------------------------------------------------------------

# ------------------------------------------------------------
# *comment


@token_required
def comment(current_user, post_id):
    """
    Comment on a post
    endpoint: /comment/<post_id>

    This method allows to comment on a post
    it can be used to get all comments for a post or add a comment to a post
    the method checks the request method
    if the request method is GET, it returns all comments for a post
    if the request method is POST, it adds a comment to a post
    also it checks before deleting a comment if the user is the author of the comment

    *GET
    *POST

    args: post_id

    return: response model according to result  

    """
    try:
        data = []
        if request.method == "GET":
            # return all comments for a post
            comment = BlogPostComments.objects(post_id=post_id)
            data.append(comment)
            response = ResponseModel(data)
            return response.get_success_response()
        elif request.method == "POST":
            # add comment to a post
            response = ResponseModel()
            json_body_form_data = request.get_json()
            _post_id = json_body_form_data["post_id"]
            _author_id = json_body_form_data["author_id"]
            _author_username = json_body_form_data["author_username"]
            _date = datetime.datetime.now()
            _comment_content = json_body_form_data["comment_content"]
            if (len(_post_id) == 0 or
                    len(_author_id) == 0 or
                    len(_comment_content) == 0):
                return response.get_bad_request_response()
            else:
                new_comment = BlogPostComments(post_id=_post_id, author_id=_author_id,
                                               date=_date, comment_content=_comment_content, author_username=_author_username)
                new_comment.save()
                data.append(new_comment)
                response.data = data
                return response.get_success_response()
        elif request.method == "DELETE":
            # delete comment
            response = ResponseModel()
            json_body_form_data = request.get_json()
            _comment_id = json_body_form_data["id"]
            post_comment = BlogPostComments.objects(id=_comment_id).first()
            if current_user.id != post_comment.author_id:
                return response.get_unauthorized_response()
            else:
                post_comment.delete()
                response.data = "comment deleted"
                return response.get_success_response()
        else:
            response = ResponseModel()
            return response.get_bad_request_response()
    except:
        response = ResponseModel()
        return response.get_bad_request_response()

# ------------------------------------------------------------

# ------------------------------------------------------------
