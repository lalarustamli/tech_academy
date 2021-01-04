import flask
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document):
    user_id = db.IntField()
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=50)
    password = db.StringField()

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def get_password(self,password):
        return check_password_hash(self.password,password)


class Course(db.Document):
    courseID = db.IntField(max_length=10)
    title = db.StringField(max_length=50)
    description = db.StringField(max_length=200)
    credits = db.IntField()
    term = db.StringField(max_length=25)

class Enrollment(db.Document):
    user_id = db.IntField()
    courseID = db.StringField(max_length=10)
