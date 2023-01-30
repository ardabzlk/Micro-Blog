from src.models.models import db


# db collection: BlogPosts


class BlogPosts(db.Document):
    """
    This class is a model for BlogPosts collection in MongoDB
    
    Attributes:
        author_id: ObjectIdField - id of the author of the post
        author_username: StringField - username of the author of the post
        title: StringField - title of the post
        content: StringField - content of the post
        date: DateField - date of the post
        category_id: IntField - id of the category of the post
        like: IntField - number of likes of the post
        dislike: IntField - number of dislikes of the post
        img_base64: StringField - base64 string of the image of the post   

    Note in order to override the default collection name, it has been set to BlogPosts

    
    """
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
    """
    This class is a model for BlogCategories collection in MongoDB

    Attributes:
        category_id: IntField - id of the category
        category_name: StringField - name of the category

    Note in order to override the default collection name, it has been set to BlogCategories
    """
    meta = {'collection': 'BlogCategories'}
    category_id = db.IntField(null=False, required=True, exists=True)
    category_name = db.StringField(null=False, required=True, exists=True)

# db collection: BlogPostComments


class BlogPostComments(db.Document):
    """
    This class is a model for BlogPostComments collection in MongoDB

    Attributes:
        post_id: ObjectIdField - id of the post
        author_id: ObjectIdField - id of the author of the comment
        author_username: StringField - username of the author of the comment
        date: DateField - date of the comment
        comment_content: StringField - content of the comment
        vote_value: IntField - value of the vote of the comment [1(like) or 2(dislike)]

    Note in order to override the default collection name, it has been set to BlogPostComments
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
    This class is a model for BlogPostVotes collection in MongoDB

    Attributes:
        post_id: ObjectIdField - id of the post
        author_id: ObjectIdField - id of the author of the vote
        vote_value: IntField - value of the vote [1(like) or 2(dislike)]

    Note in order to override the default collection name, it has been set to BlogPostVotes        
    """
    meta = {'collection': 'BlogPostVotes'}
    post_id = db.ObjectIdField()
    author_id = db.ObjectIdField()
    vote_value = db.IntField()
