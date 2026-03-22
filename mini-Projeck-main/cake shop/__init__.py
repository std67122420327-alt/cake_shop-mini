import os
from flask import Flask
from foodapp.extensions import db, login_manager, bcrypt
from foodapp.models import User, Category, Food
from foodapp.core.routes import core_bp
from foodapp.users.routes import user_bp
from foodapp.foods.routes import food_bp

# Load environment variables from .env file (for local development only)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, using system environment variables (production)

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'warning'
    login_manager.login_message = 'Please log in to access this page.'
    bcrypt.init_app(app)

    app.register_blueprint(core_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(food_bp, url_prefix='/food')

    return app