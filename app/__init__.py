from flask import Flask
from firebase_admin import credentials, initialize_app
from pymongo import MongoClient
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    cred = credentials.Certificate(r"C:\Users\Keshav\OneDrive\Desktop\bookrentalbackend\keshav-bookrental-firebase-adminsdk-fbsvc-907d53c33d.json")
    initialize_app(cred)

    client = MongoClient(app.config['MONGODB_URI'])
    app.db = client[app.config['DATABASE_NAME']]

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    @app.route('/test')
    def test_route():
        return 'Test route is working!'

    return app
