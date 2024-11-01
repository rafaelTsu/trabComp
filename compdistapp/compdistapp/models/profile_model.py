from .database import db
import os

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(65), unique=True, nullable=True)
    registered = db.Column(db.DateTime(timezone=True), default=db.func.now())

    def insert_admin():
        admin_user = os.getenv("ADMIN_USER", "brivaldo")
        admin_password = os.getenv("ADMIN_PASSWORD", "123")
        user = db.session.execute(db.select(Profile).filter_by(username=admin_user)).scalar()

        if not user:
            profile = Profile(username=admin_user, password=admin_password)
            db.session.add(profile)
            db.session.commit()
            print("Administrador inserido com sucesso")
        
        else:
            print("Administrador ja inserido")
    
    def __repr__(self):
        return f"<Profile {self.username}>"