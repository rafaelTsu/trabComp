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

from services.auth import auth, AuthException, validate_authentication

class MyModelView(ModelView):
    def is_accessible(self):
        from app import app
        if auth.get_auth():
            username = auth.get_auth()['username']
            password = auth.get_auth()['password']
        else:
            username = None
            password = None

        if username and password:
            if validate_authentication(username, password) and username in os.getenv('ADMIN_USER'):
                return True
            else:
                raise AuthException('Not authenticated.')
        else:
            raise AuthException('Not authenticated.')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(auth.login_required())

class ProfileView(MyModelView):
    column_exclude_list = ['password', ]
    column_searchable_list = ['username', ]
    can_export = True
    can_view_details = True
