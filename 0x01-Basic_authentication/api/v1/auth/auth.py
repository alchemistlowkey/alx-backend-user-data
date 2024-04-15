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
        return False

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
