#!/usr/bin/env python3
"""
A Flask view that handles all routes for the Session authentication.
"""
from flask import jsonify, request, abort
from models.user import User
from api.v1.views import app_views
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    Session Login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    for users in user:
        if users.is_valid_password(password):
            user_id = users.id
            from api.v1.app import auth
            session_id = auth.create_session(user_id)
            response = jsonify(users.to_json())
            response.set_cookie(os.getenv('SESSION_NAME'), session_id)
            return response
        return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404
