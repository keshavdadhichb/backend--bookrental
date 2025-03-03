from flask import Blueprint, request, jsonify, current_app
from bson import json_util
import json

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        name = request.args.get('name')
        email = request.args.get('email')

        # Start with an empty filter
        filter_query = {}

        # Add filters if provided
        if name:
            filter_query['name'] = {'$regex': name, '$options': 'i'}  # Case-insensitive regex match
        if email:
            filter_query['email'] = {'$regex': email, '$options': 'i'}

        # Calculate skip value for pagination
        skip = (page - 1) * per_page

        # Query the database
        users = list(current_app.db.users.find(filter_query).skip(skip).limit(per_page))

        # Get total count for pagination
        total_users = current_app.db.users.count_documents(filter_query)

        # Convert ObjectId to string for JSON serialization
        users = json.loads(json_util.dumps(users))

        # Prepare response
        response = {
            'users': users,
            'page': page,
            'per_page': per_page,
            'total_users': total_users,
            'total_pages': (total_users + per_page - 1) // per_page
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<uid>', methods=['GET'])
def get_user(uid):
    try:
        user = current_app.db.users.find_one({'uid': uid})
        if user:
            # Convert ObjectId to string for JSON serialization
            user = json.loads(json_util.dumps(user))
            return jsonify(user), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<uid>', methods=['PUT'])
def update_user(uid):
    try:
        data = request.json
        result = current_app.db.users.update_one({'uid': uid}, {'$set': data})
        if result.modified_count:
            return jsonify({'message': 'User updated successfully'}), 200
        return jsonify({'error': 'User not found or no changes made'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<uid>', methods=['DELETE'])
def delete_user(uid):
    try:
        result = current_app.db.users.delete_one({'uid': uid})
        if result.deleted_count:
            return jsonify({'message': 'User deleted successfully'}), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
