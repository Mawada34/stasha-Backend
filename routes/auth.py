from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    password = data.get("password")

    if not password:
        return jsonify({"error": "Password required"}), 400

    stored_hash = os.environ.get("ADMIN_PASSWORD_HASH")

    if not check_password_hash(stored_hash, password):
        return jsonify({"error": "Invalid password"}), 401

    token = create_access_token(identity="admin")
    return jsonify({"token": token})