from flask import Flask, request, jsonify, g
from firebase_admin import credentials, initialize_app, auth
from pymongo import MongoClient
from config import Config
from .users.routes import users_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Firebase
    try:
        cred = credentials.Certificate("C:\\Users\\Keshav\\OneDrive\\Desktop\\backend--bookrental\\keshav-bookrental-firebase-adminsdk-fbsvc-06914d8390.json")
        initialize_app(cred)
        print("Successfully initialized Firebase!")
    except Exception as e:
        print(f"Failed to initialize Firebase: {str(e)}")
        # Properly handle Firebase initialization failure based on your needs
        raise

    # Initialize MongoDB outside of request context
    try:
        app.client = MongoClient(app.config['MONGODB_URI'])
        app.db = app.client[app.config['DATABASE_NAME']]
        print("Successfully connected to MongoDB during app initialization!")
    except Exception as e:
        print(f"Failed to connect to MongoDB during app initialization: {str(e)}")
        # It's best to raise here to prevent the app from running without a DB connection.
        raise

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    @app.route('/')
    def index():
        return "Home"

    @app.route('/keshav')
    def about():
        return "keshavdadhich"

    @app.route('/test')
    def test_route():
        return 'Test route is working!'

    return app

