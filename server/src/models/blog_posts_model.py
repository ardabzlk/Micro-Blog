from src.models.models import db


# db collection: BlogPosts


class BlogPosts(db.Document):
    meta = {'collection': 'BlogPosts'}
    author_id = db.ObjectIdField(null=False, required=True, exists=True)
    author_username = db.StringField(null=False, required=True, exists=True)
    title = db.StringField(null=False, required=True, exists=True)
    content = db.StringField(null=False, required=True, exists=True)
    date = db.DateField(null=False, required=True, exists=True)
    category_id = db.IntField(null=False, required=True, exists=True)
    like = db.IntField()
    dislike = db.IntField()
    img_base64 = db.StringField(null=False, required=True, exists=True)

# db collection: BlogCategories


class BlogCategories(db.Document):
    meta = {'collection': 'BlogCategories'}
    category_id = db.IntField(null=False, required=True, exists=True)
    category_name = db.StringField(null=False, required=True, exists=True)

# db collection: BlogPostComments


class BlogPostComments(db.Document):
    """
    user_id: id field
    post_id: id field
    vote_value: 0(no vote),1
    """
    meta = {'collection': 'BlogPostComments'}
    post_id = db.ObjectIdField()
    author_id = db.ObjectIdField()
    author_username = db.StringField()
    date = db.DateField()
    comment_content = db.StringField()
    vote_value: db.IntField()

# db collection: BlogPostVotes


class BlogPostVotes(db.Document):

    """
    user_id: id field
    post_id: id field
    vote_value: 0(no vote),1
    """
    meta = {'collection': 'BlogPostVotes'}
    post_id = db.ObjectIdField()
    author_id = db.ObjectIdField()
    vote_value = db.IntField()
