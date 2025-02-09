from flask import Blueprint, request, jsonify
from app.models import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = list(users_bp.app.db.be.users.find())
    return jsonify([User(**user).to_dict() for user in users]), 200

@users_bp.route('/users/<uid>', methods=['GET'])
def get_user(uid):
    user = users_bp.app.db.be.users.find_one({'uid': uid})
    if user:
        return jsonify(User(**user).to_dict()), 200
    return jsonify({'error': 'User not found'}), 404

@users_bp.route('/users/<uid>', methods=['PUT'])
def update_user(uid):
    data = request.json
    result = users_bp.app.db.be.users.update_one({'uid': uid}, {'$set': data})
    if result.modified_count:
        return jsonify({'message': 'User updated'}), 200
    return jsonify({'error': 'User not found'}), 404

@users_bp.route('/users/<uid>', methods=['DELETE'])
def delete_user(uid):
    result = users_bp.app.db.be.users.delete_one({'uid': uid})
    if result.deleted_count:
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'error': 'User not found'}), 404
