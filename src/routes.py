from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User, user_schema, users_schema, db 

app = Blueprint("app",__name__)

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
        hashed_password = generate_password_hash(password)
        newUser = User(username=username,password=hashed_password,email=email)
        try:
            db.session.add(newUser)
            db.session.commit()
            return user_schema.jsonify(newUser)
        except Exception as e:
            print(e)
            return jsonify({'msg':'Error in creating new user'})

@app.route('/login',methods=['POST'])
def login():
    if request.method=='POST':
        username = request.json['username']
        password = request.json['password']
        if User.query.filter_by(username=username).count():
            targetUser = User.query.filter_by(username=username).first()
            if check_password_hash(targetUser.password,password):
                return jsonify({'msg':'User Logged in'})
            else:
                return jsonify({'msg':'Wrong password'})
        else:
            return jsonify({'msg':'User not registered'})


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
