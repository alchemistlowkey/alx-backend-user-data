#!/usr/bin/env python3
"""
Add an expiration date to a Session ID
"""
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    Session Authentication with expiration
    """

    def __init__(self):
        """
        Initializes class
        """
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION')) if \
            getenv('SESSION_DURATION') else 0

    def create_session(self, user_id=None):
        """
        Create a Seesion ID with expiration
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Get the user ID for a given Session ID with expiration
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']
        if 'created_at' not in session_dict:
            return None
        expiration_date = session_dict['created_at'] + \
            timedelta(seconds=self.session_duration)
        if expiration_date < datetime.now():
            return None
        return session_dict['user_id']
