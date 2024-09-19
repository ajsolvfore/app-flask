from flask import Flask
from src.routes.order_routes import order_blueprint
from src.models.order_model import db
import os
from dotenv import load_dotenv
from src.routes.user_routes import user_blueprint
from src.routes.product_routes import product_blueprint
from src.routes.auth_routes import auth_blueprint
from flask_jwt_extended import JWTManager
from src.utils.encryption import bcrypt

# Load environment variables from .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Flask secret key
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')  # JWT secret key

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(order_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(auth_blueprint)
    return app
