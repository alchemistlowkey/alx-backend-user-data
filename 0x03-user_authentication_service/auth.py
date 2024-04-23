from bcrypt import hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
        """
        Hash a password using bcrypt

        Args:
            password (str): The password to hash

        Returns:
            bytes: Salted hash of the input password
        """

        salted = gensalt()

        hashed_input_password = hashpw(password.encode('utf-8'), salted)

        return hashed_input_password


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user

        Args:
            email (str): Email of the user
            password (str): Password of the user

        Returns:
            User: The newly registered User object

        Raises:
            ValueError: If a user already exists with the provided email
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=hashed_password)
            return user
