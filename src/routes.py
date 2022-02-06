from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User, user_schema, users_schema, db 
from http import HTTPStatus
from flask_restful import Resource, Api
app = Blueprint("app",__name__)
api = Api(app)

# @app.route('/',methods=['GET'])
# def index():
#     return jsonify({'msg':'Hellooooooo'})

class Home(Resource):
    def get(self):
        return "HelloBhai"
api.add_resource(Home,'/')

#creating user 
# @app.route('/signup',methods=['POST'])
# def signup():
class Signup(Resource):
    def POST(self):
        # if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        hashed_password = generate_password_hash(password)
        newUser = User(username=username,password=hashed_password,email=email)
        try:
            db.session.add(newUser)
            db.session.commit()
            return user_schema.jsonify(newUser)
        except Exception as e:
            print(e)
            return jsonify({'msg':'Error in creating new user'}) , HTTPStatus.BAD_REQUEST

# @app.route('/login',methods=['POST'])
class Login(Resource):
    def post(self):
        # if request.method=='POST':
        username = request.json['username']
        password = request.json['password']
        if User.query.filter_by(username=username).count():
            targetUser = User.query.filter_by(username=username).first()
            if check_password_hash(targetUser.password,password):
                return {'msg':'User Logged in'} ,HTTPStatus.OK
            else:
                return {'msg':'Wrong password'}
        else:
            return {'msg':'User not registered'}

api.add_resource(Signup,'/signup')
api.add_resource(Login, '/login')

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
