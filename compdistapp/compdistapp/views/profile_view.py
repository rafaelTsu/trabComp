from flask_admin.contrib.sqla import ModelView
from flask import redirect
from werkzeug.exceptions import HTTPException
from flask_httpauth import HTTPBasicAuth

# Autenticação e app precisam ser importados de app.py ou definidos globalmente
from app import auth, validate_authentication, app

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})
        )

class MyModelView(ModelView):
    def is_accessible(self):
        auth_data = auth.get_auth()
        username = auth_data.get('username') if auth_data else None
        password = auth_data.get('password') if auth_data else None

        if username and password:
            if validate_authentication(username, password) and username in app.config.get('ADMINISTRATORS'):
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
