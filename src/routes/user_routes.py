from flask import Blueprint, request, jsonify
from src import db
from src.models.users_model import User
from flask_jwt_extended import jwt_required,  get_jwt_identity
from src.utils.encryption import generate_password_hash

# Define the blueprint for user-related routes
user_blueprint = Blueprint('users', __name__, url_prefix='/user')

# Route to get all users (authentication required)
@user_blueprint.route('/get_users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.as_dict() for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to add a new user (authentication required)
@user_blueprint.route('/add', methods=['POST'])
def add_user():
    try:
        new_user_data = request.json
        password = new_user_data.get("password")
        
        if not password:
            return jsonify({"error": "Password is required"}), 400
        
        hashed_password = generate_password_hash(password)
        
        user = User(
            name=new_user_data['name'],
            email=new_user_data['email'],
            encrypted_password=hashed_password
        )
        
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User added successfully', 'user': user.as_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get a specific user by ID (authentication required)
@user_blueprint.route('/get_user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.as_dict())
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a user by ID (authentication required)
@user_blueprint.route('/delete_user/<uuid:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
