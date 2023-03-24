from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
# db has MongoEngine, So we can import Fields such as StringFields, etc
# docs.mongoengine.org/apireference.html#fields

# return active user.
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    # username field
    username = db.StringField(unique=True, required=True)

    # email field
    email = db.EmailField(unique=True, required=True)

    # password field
    password = db.StringField()

    # profile_pic field
    profile_pic = db.ImageField()

    # dark_mode field
    dark_mode = db.BooleanField(default=False)
    
    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class Review(db.Document):
    # user field - reference to the User who commented
    commenter = db.ReferenceField(User, required=True)

    # content field - with length between 5 and 500 characters
    content = db.StringField(min_length=5, max_length=500, required=True)

    # date field - saved as a string instead of a datetime
    date = db.StringField(required=True)

    # imdb_id field - with length 9
    imdb_id = db.StringField(min_length=8, max_length=10, required=True)

    # movie_title field - with length between 1 and 100 characters
    movie_title = db.StringField(min_length=1, max_length=100, required=True)
