#!/usr/bin/env python3
"""
BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    BasicAuth class to manage API
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        A base64 Authorization method
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        A method that returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_size = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_size.decode('utf-8')
            return decoded_str
        except Exception as err:
            return None
