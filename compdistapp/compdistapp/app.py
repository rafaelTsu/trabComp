# Importe apenas o necessário e evite importar SQLAlchemy e Admin duas vezes
from flask import Flask, Response, redirect, jsonify, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash

from models.database import db
from models.profile_model import Profile 
from views.profile_view import ProfileView  # Importando a ProfileView já configurada

# Configuração básica da aplicação Flask
app = Flask("Comp Dist")
auth = HTTPBasicAuth()

# Configuração
app.config.from_pyfile('cfg/app.cfg', silent=True)
app.secret_key = app.config.get('SECRET_KEY')
app.config['FLASK_ADMIN_SWATCH'] = 'yeti'
app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('DATABASE')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ADMINISTRATORS'] = ['admin']  # Exemplo, ajuste conforme necessário

# Inicialize o db e a migração
db.init_app(app)
migrate = Migrate(app, db)

# Inicialize o Admin com a View personalizada
admin = Admin(app, name='Super App', template_mode='bootstrap4')
admin.add_view(ProfileView(Profile, db.session))

# Função de verificação de senha
@auth.verify_password
def verify_password(username, password):
    user = Profile.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return username

# Validação de autenticação para o Flask-Admin
def validate_authentication(username, password):
    user = Profile.query.filter_by(username=username).first()
    return user and check_password_hash(user.password, password)

# Rota principal
@app.route('/')
@auth.login_required
def index():
    user = auth.current_user()

    user_db = Profile.query.filter(Profile.username == user).first()
    if user_db:
        message_info = f"Usuário {user}, acessou o index."
        log.info(message_info)
        return jsonify({"success": message_info})

# Inicializar a aplicação
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", debug=True, port=8080)
