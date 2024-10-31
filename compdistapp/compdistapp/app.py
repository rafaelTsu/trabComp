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

from models.database import db

# Application log
logging.basicConfig(format='%(asctime)s - %(message)s', filename="log/app.log", level=logging.INFO)
log = logging.getLogger()

# Web Application name
app = Flask("Comp Dist")

# Configuration
app.config.from_pyfile('cfg/app.cfg', silent=True)
app.config['FLASK_SECRET'] = os.environ('SECRET_KEY')
app.config['BASIC_AUTH_FORCE'] = True
app.secret_key = os.environ('SECRET_KEY')

# Set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'yeti'

# adding configuration for using a database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from views.profile_view import ProfileView
from models.profile_model import Profile
# Admin Interface
admin = Admin(app, name='Super App', template_mode='bootstrap4')
admin.add_view(ProfileView(Profile, db.session))


from services.auth import auth
# Routes
@app.route('/')
@auth.login_required
def index():
    user = auth.current_user()

    # Check if the user exist
    user_db = Profile.query.filter(Profile.username == user)

    # Avoid error while checking the users in database
    user_list = False
    try:
        user_list = user_db.all()[0]
    except IndexError:
        pass

    if user_list:
        message_info = f"Usuário {user}, acessou o index."

        response = {"success": message_info}
        log.info(message_info)

        return jsonify(response)


# Initialize the application
if __name__ == "__main__":
    import time
    time.sleep(20)
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", debug=True, port=8080)
