#!/usr/bin/env python3
"""
Sessions in database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Session Authentication with Session ID stored in database
    """

    def create_session(self, user_id=None):
        """
        Create a Session Id and store it in the database
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Get the user ID from the database based on the Session ID
        """
        if session_id is None:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None
        session_dict = user_session[0]
        if self.session_duration <= 0:
            return session_dict.user_id
        expiration_date = session_dict.created_at + \
            timedelta(seconds=self.session_duration)
        if expiration_date < datetime.now():
            return None
        return session_dict.user_id

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on the Session ID
        from the request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False
        user_session.remove()
        return True
