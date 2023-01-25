from src.models.models import db


# db collection: blog_posts


class blogPosts(db.Document):

    author_id = db.ObjectIdField(null=False, required=True, exists=True)
    author_username = db.StringField(null=False, required=True, exists=True)
    title = db.StringField(null=False, required=True, exists=True)
    content = db.StringField(null=False, required=True, exists=True)
    date = db.DateField(null=False, required=True, exists=True)
    category_id = db.IntField(null=False, required=True, exists=True)
    like = db.IntField()
    dislike = db.IntField()
    img_base64 = db.StringField(null=False, required=True, exists=True)

# db collection: blog_categories


class blogCategories(db.Document):

    category_id = db.IntField(null=False, required=True, exists=True)
    category_name = db.StringField(null=False, required=True, exists=True)

# db collection: blog_post_comments


class blogPostComments(db.Document):
    """
    user_id: id field
    post_id: id field
    vote_value: 0(no vote),1
    """
    post_id = db.ObjectIdField()
    author_id = db.ObjectIdField()
    author_username = db.StringField()
    date = db.DateField()
    comment_content = db.StringField()
    vote_value: db.IntField()

# db collection: blog_post_votes


class blogPostVotes(db.Document):

    """
    user_id: id field
    post_id: id field
    vote_value: 0(no vote),1
    """
    post_id = db.ObjectIdField()
    author_id = db.ObjectIdField()
    vote_value = db.IntField()
