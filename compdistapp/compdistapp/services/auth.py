import logging
import os
from flask import Flask, Response, redirect, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException

from models.profile_model import Profile

auth = HTTPBasicAuth()

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})
        )

# Authentication control
@auth.verify_password
def verify_password(username, password):
    user = Profile.query.filter(Profile.username == username)

    if user.all():
        user_query = user.all()[0]
        if check_password_hash(generate_password_hash(user_query.password), password):
            return username


# Protect the Flask-Admin using username/password strings and SQLAlchemy
def validate_authentication(username, password):
    user = Profile.query.filter(Profile.username == username)

    if user.all():
        user_query = user.all()[0]
        if user_query.password == password:
            return True
        return False
    return False