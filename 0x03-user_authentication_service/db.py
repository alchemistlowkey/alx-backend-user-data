#!/usr/bin/env python3

"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        add_user method

        Args:
            email (str): Email of the user
            hashed_password (str): Hashed password of the user

        Returns:
            User: The newly created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by specified keyword arguments

        Args:
            **kwargs: Arbitrary keyword arguments to filter users

        Returns:
            User: The first user found matching the filter criteria

        Raises:
            NoResultFound: If no results are found(Not found)
            InvalidRequestError: If wrong query arguments are passed(Invalid)
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        User update method

        Args:
            user_id (int):
                The ID of the user to update
            **kwargs:
                Arbitrary keyword args representing user attributes to update

        Raises:
            ValueError:
                If an arg that does'nt correspond to a user attribute is passed
        """

        user = self.find_user_by(id=user_id)

        for attribute, value in kwargs.items():
            if hasattr(user, attribute):
                setattr(user, attribute, value)
            else:
                raise ValueError

        self._session.commit()
