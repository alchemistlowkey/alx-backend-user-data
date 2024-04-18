#!/usr/bin/env python3
"""
SessionAuth class
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    SessionAuth class to manage API
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        An instance method that creates a session ID for a user_ID
        """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        An instance method that returns a user ID based on a session ID
        """

        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        An instance method (overload) that returns a User instance
        based on a cookie value
        """

        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)
