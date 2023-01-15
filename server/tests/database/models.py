from mongoengine import Document, StringField


class User(Document):
    """
    User model for user collection
    user_id
    name
    surname
    """
    name = StringField(null=False, required=True, exists=True)
    surname = StringField(null=False, required=True, exists=True)
    username = StringField(null=False, required=True, exists=True)
    email = StringField(null=False, required=True, exists=True)
    password = StringField(null=False, required=True, exists=True)
