from flask import Flask
from src.routes import app
import os

def create_app():
    app1 = Flask(__name__)
    app1.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app1.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://mohtashimkamran:kamran@127.0.0.1/test.db'
    from src.models import db, marsh
    db.app=app1
    db.init_app(app1)
    marsh.init_app(app1)

    app1.register_blueprint(app)
    
    return app1
