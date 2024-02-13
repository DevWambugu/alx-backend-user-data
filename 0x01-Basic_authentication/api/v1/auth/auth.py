#!/usr/bin/env python3
"auth class"


from flask import request
from typing import List, TypeVar
from tabnanny import check


class Auth:
    '''This class contains methods that manage
    the API authentication'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''returns False'''
        check = path
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            check += "/"
        if check in excluded_paths or path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        '''returns None'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''returns None'''
        return None
