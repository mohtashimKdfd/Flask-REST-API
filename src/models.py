from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy()
# init marshmallow
marsh = Marshmallow()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String,nullable=False, unique=True)
    email = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)

    # def __repr__(self):
        # return self.username
    def __init__(self,username,email,password):
        # self.id=id 
        self.username = username
        self.email = email
        self.password = password
        

class UserSchema(marsh.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')

#Initiliasing Schema

user_schema = UserSchema()

users_schema = UserSchema(many=True)