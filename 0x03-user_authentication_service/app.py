#!/usr/bin/env python3
'''Basic flask app'''

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def bienvenue() -> str:
    '''This function returns a JSON payload of the form
    {"message": "Bienvenue"}
    '''
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def user() -> str:
    '''implements the end-point to register a user'''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''implement a login function to
    respond to the POST /sessions route'''
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if valid_login:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
