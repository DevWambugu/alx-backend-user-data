#!/usr/bin/env python3
'''auth'''


from db import DB
from typing import TypeVar
from user import User
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound

def _hash_password(password: str) -> str:
    """
    This method that takes in a password
    string arguments and returns bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def generate_string_uuid() -> str:
    '''returns a string representation of a new UUID'''
    return str(uuid4())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
         take mandatory email and password string
         arguments and return a User object.
         If a user already exist with the passed email, raise
         a ValueError with the message User <user's email>
         already exists. If not, hash the password
         with _hash_password, save the user to the
         database using self._db and return the User object
         """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        ''' implements the Auth.valid_login method'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        '''takes an email string argument and
        returns the session ID as a string'''
        try:
            user = self._db.find_user_by(email=email)
            sess_id = generate_string_uuid()
            self._db.update_user(user.id, session_id=sess_id)
            return sess_id
        except NoResultFound:
            return
