from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow #marshmallow is a library for serialization/deserialization of data
import os

#Initiliasing app
app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return jsonify({'msg':'Hell YEAHHHHHHH!!!!!'})

if __name__ == '__main__':
    app.run(debug=True)