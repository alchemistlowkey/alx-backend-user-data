#!/usr/bin/env python3
"""
Auth class
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Auth class to manage API
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Auth required method
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        if path == excluded_paths:
            return False
        if not path.endswith("/"):
            path += "/"
        for excluded_path in excluded_paths:
            if excluded_path.endswith("/"):
                if path.startswith(excluded_path):
                    return False
            if excluded_path.endswith("*") and \
                    path.startswith(excluded_path[:-1]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Authorization header method
        """
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Current User method
        """
        return None

    def session_cookie(self, request=None):
        """
        A method that returns a cookie value from a request
        """

        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
