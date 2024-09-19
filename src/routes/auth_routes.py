from flask import Blueprint, request, jsonify
from src.models.users_model import User
from flask_jwt_extended import create_access_token
from src.utils.encryption import check_password_hash

# Define the blueprint for authentication-related routes
auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

# Route to authenticate a user and return a JWT token
@auth_blueprint.route("/token", methods=["POST"])
def create_token():
    try:
        email = request.json["email"]
        password = request.json["password"]

        user = User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.encrypted_password, password):
            return jsonify({"error": "Unauthorized"}), 401

        access_token = create_access_token(identity=user.id)

        return jsonify({
            "id": str(user.id),
            "email": user.email,
            "access_token": access_token,
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
