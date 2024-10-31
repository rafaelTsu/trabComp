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

def create_admin():
    """Cria o usuário admin se ele não existir."""
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin")
    
    # Verifica se o usuário administrador já existe
    existing_user = Profile.query.filter_by(username=admin_username).first()
    
    if not existing_user:
        # Adiciona o usuário administrador ao banco de dados
        admin_user = Profile(
            username=admin_username, 
            password=generate_password_hash(admin_password)
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Usuario admin criado com sucesso")