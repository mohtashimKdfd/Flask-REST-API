import bcrypt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow #marshmallow is a library for serialization/deserialization of data
import os

#Initiliasing app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://mohtashimkamran:kamran@127.0.0.1/test.db'

# init db
db = SQLAlchemy(app)
# init marshmallow
marsh = Marshmallow(app)

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


#hashing password
def password_hashing(password):
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

def check_password(password,hashed_password):
    hashed = bcrypt.hashpw(hashed_password.encode('utf-8'),bcrypt.gensalt())
    return bcrypt.checkpw(password.encode('utf8'), hashed)
    

@app.route('/',methods=['GET'])
def index():
    return jsonify({'msg':'Hellooooooo'})

#creating user 
@app.route('/signup',methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        hashed_password = password_hashing(password)
        newUser = User(username=username,password=hashed_password,email=email)
        try:
            db.session.add(newUser)
            db.session.commit()
            return user_schema.jsonify(newUser)
        except Exception as e:
            print(e)
            return jsonify({'msg':'Error in creating new user'})

# @app.route('/login',methods=['POST'])
# def login():
#     if request.method=='POST':
#         username = request.json['username']
#         password = request.json['password']
#         if User.query.filter_by(username=username).count():
#             targetUser = User.query.filter_by(username=username).first()
#             if check_password(password,targetUser.password):
#                 return jsonify({'msg':'User Logged in'})
#             else:
#                 return jsonify({'msg':'Wrong password'})
#         else:
#             return jsonify({'msg':'User not registered'})


@app.route('/allusers',methods=['GET'])
def getusers():
    allusers = User.query.all()
    if len(allusers) == 0:
        return jsonify({'msg':'No user found'})
    return users_schema.jsonify(allusers)

@app.route('/remove/<int:id>',methods=['DELETE'])
def delete(id):
    targetUser = User.query.get(id)
    db.session.delete(targetUser)
    db.session.commit()
    return jsonify({'msg':'User deleted'})

if __name__ == '__main__':
    app.run(debug=True)