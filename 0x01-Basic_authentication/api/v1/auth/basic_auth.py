#!/usr/bin/env python3
"""
basic_auth
"""

from api.v1.auth.auth import Auth
from typing import TypeVar, List
from models.user import User
import base64
import binascii


class BasicAuth(Auth):
    '''this is the class BasicAuth'''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''This method  returns the Base64
        part of the Authorization header
        for a Basic Authentication'''
        if (authorization_header is None or
                not isinstance(authorization_header, str) or
                not authorization_header.startswith("Basic")):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''This method returns the decoded value
        of a Base64 string base64_authorization_header'''
        b64_auth_header = base64_authorization_header
        if b64_auth_header and isinstance(b64_auth_header, str):
            try:
                encode = b64_auth_header.encode('utf-8')
                base = base64.b64decode(encode)
                return base.decode('utf-8')
            except binascii.Error:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''This method returns the user email and password
        from the Base64 decoded value'''
        if (decoded_64 and isinstance(decoded_64, str) and
                ":" in decoded_64):
            res = decoded_64.rsplit(":", 1)
            if len(res) == 2:
                return (res[0], res[1])
        return(None, None)

    def user_object_from_credentials(self, user_email:
                                     str, user_pwd: str) -> TypeVar('User'):
        '''This method returns the User instance based
        on his email and password'''
        if not user_email or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user = User.search(user_email)
        if user is None:
            return None
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        '''This method overloads Auth and retrieves the User
        instance for a request. This method protects your API'''
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_credentials = \
            self.extract_base64_authorization_header(auth_header)
        if base64_credentials is None:
            return None
        user_credentials = \
            self.decode_base64_authorization_header(base64_credentials)
        if user_credentials is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(user_credentials)
        if user_email is None or user_pwd is None:
            return None
        return user
