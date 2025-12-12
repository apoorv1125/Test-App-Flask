from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testuser.db'

    app.secret_key = 'SECRET'
    
    app.config['SECRET_KEY'] = 'SECRET'

    db.init_app(app)
 
    bcrypt = Bcrypt(app)

    from routes import register_route
    register_route(app = app, db = db, bcrypt = bcrypt)

    return app