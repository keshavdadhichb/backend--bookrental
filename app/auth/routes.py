from flask import Blueprint, request, jsonify, g
from firebase_admin import auth as firebase_auth, exceptions
from bson import json_util
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if not email or not password or not name:
            return jsonify({'error': 'Missing email, password, or name'}), 400

        if not email.endswith('@vitstudent.ac.in'):
            return jsonify({'error': 'Please login with vit email id only'}), 400

        try:
            user = firebase_auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
        except exceptions.FirebaseError as firebase_err:
            return jsonify({'error': f'Firebase signup error: {str(firebase_err)}'}), 400

        uid = user.uid
        user_data = {
            'uid': uid,
            'name': name,
            'email': email,
        }

        # Insert user data into MongoDB
        try:
            from flask import current_app
            current_app.db.users.insert_one(user_data)
            print("User data inserted successfully!")
        except Exception as db_error:
            return jsonify({'error': f'Database error: {str(db_error)}'}), 500

        return jsonify({'message': 'User created successfully', 'uid': uid}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        token = data.get('token')
        if not token:
            return jsonify({'error': 'Missing token'}), 400
        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token['uid']
        #Token is valid
        return jsonify({'message': 'Login successful', 'uid': uid}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
