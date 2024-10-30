from .database import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(65), unique=True, nullable=True)
    registered = db.Column(db.DateTime(timezone=True), default=db.func.now())

    def __repr__(self):
        return f"<Profile {self.username}>"