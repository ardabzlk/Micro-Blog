from flask import request, make_response
from src.models.blog_posts_model import BlogPosts, BlogCategories, BlogPostComments, BlogPostVotes
import datetime
from src.services.JWT_service import token_required
from src.models.models import ResponseModel

"""
def ExampleCRUDMethod():
'''Docstring for ExampleCRUDMethod'''

    try:
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
    except:
        response = ResponseModel()
        return response.get_bad_request_response()
"""

# ------------------------------------------------------------
# */blog_posts/<param_post_id>


@token_required
def post_management(current_user, param_post_id):
    """Manage single post
    it can be used to get, update or delete a single post
    it checks if the user is the author of the post before updating or deleting it-
    by comparing the current user id with the author id
    endpoint: /blog-posts/<param_post_id>


    Parameters
    ----------
    param_post_id: str
        id of the post to be managed

    Returns
    -------
    json
        response model according request method and result

    Exceptions
    ----------
    Exception if request method is not valid
    ResponseModel.get_bad_request_response()

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
    """Manage all posts
    it can be used to get all posts or add a new post
    endpoint: /blog-posts

    Parameters
    ----------
    none

    Returns
    -------
    json
        response model according request method and result if successfull
        it can return a list of posts or a single post if its new

    Exceptions
    ----------
    Exception if request method is not valid
    ResponseModel.get_bad_request_response()
    """
    # *POST
    # add new blog post
    try:
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
    except:
        response = ResponseModel()
        return response.get_bad_request_response()
# ------------------------------------------------------------


@token_required
def vote(current_user):
    """Vote for a post
    it can be used to like or dislike a post
    it checks if the user has already voted for the post before
    if the user has already voted for the post, it updates the vote
    if the user has not voted for the post, it adds a new vote
    endpoint: /vote

    Parameters
    ----------
    post_id: str
        the id of the post to vote for
    author_id: str
        the id of the user who votes
    vote_value: int
        the value of the vote(1: like, 2: dislike)

    Returns
    -------
    json
        success response model if successfull

    Exceptions
    ----------
    Bad request response model if the request is not valid
    ResponseModel.get_bad_request_response()


    """

    response = ResponseModel()
    json_body_form_data = request.get_json()
    _post_id = json_body_form_data["post_id"]
    _author_id = json_body_form_data["author_id"]
    _vote_value = json_body_form_data["vote_value"]
    try:
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
    except:
        response = ResponseModel()
        return response.get_bad_request_response()


# ------------------------------------------------------------


# ------------------------------------------------------------
# * blog categories


@token_required
def blog_post_categories(current_user):
    """ Blog post categories Management
    this endpoint is used to get all blog post categories, add a new category or delete a category
    if the request method is GET, it returns all blog post categories
    if the request method is POST, it adds a new category
    if the request method is DELETE, it deletes a category
    it does not have authorization checks before deleteing a category
    it increments the category id by 1 for each new category
    
    endpoint: /blog_post_categories

    Parameters
    ----------
    category_name: str
        the name of the category
    category_id: int
        the id of the category
    
    Returns
    -------
    json
        success response model if successfull

    Exceptions
    ----------
    Bad request response model if the request is not valid
    ResponseModel.get_bad_request_response()

    
    """
    try:
        if request.method == "GET":
            data = []
            for category in BlogCategories.objects():
                data.append(category)
            response = ResponseModel(data)
            return response.get_success_response()
        elif request.method == "POST":
            body_form_data = request.get_json()
            latest_category = BlogCategories.objects().order_by('-category_id').first()
            if(latest_category != None):
                    latest_category_id = latest_category.category_id + 1
            elif(latest_category == None):
                latest_category_id = 1

            blog_post_category = BlogCategories(
                category_id=latest_category_id, category_name=body_form_data.get("category_name"))
            blog_post_category.save()
            data = []
            data.append(blog_post_category)
            response = ResponseModel(data)
            return response.get_success_response()
        elif request.method == "DELETE":
            body_form_data = request.get_json()
            category_id = body_form_data.get("category_id")
            BlogCategories.objects(category_id=category_id).delete()
            response = ResponseModel()
            return response.get_success_response()
    except:
        response = ResponseModel()
        return response.get_bad_request_response()

# ------------------------------------------------------------

# ------------------------------------------------------------
# *comment


@token_required
def comment(current_user, post_id):
    """Comment on a post
    This method allows to comment on a post
    it can be used to get all comments for a post or add a comment to a post
    the method checks the request method
    if the request method is GET, it returns all comments for a post
    if the request method is POST, it adds a comment to a post
    also it checks before deleting a comment if the user is the author of the comment
    endpoint: /comment/<post_id>

    Parameters
    ----------
    post_id: str
        the id of the post to comment on
    author_id: str
        the id of the user who comments
    author_username: str
        the username of the user who comments
    comment_content: str
        the comment


    Returns
    -------
    json
        post method:
            success response model if successfull
        get method:
            particular comment if successfull

    Exceptions
    ----------
    Bad request response model if the request is not valid
    ResponseModel.get_bad_request_response()

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
