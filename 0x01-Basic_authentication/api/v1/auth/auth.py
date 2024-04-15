#!/usr/bin/env python3
"""
Auth class
"""
from flask import request
from typing import List, TypeVar


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
        return True

    def authorization_header(self, request=None) -> str:
        """
        Authorization header method
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Current User method
        """
        return None
