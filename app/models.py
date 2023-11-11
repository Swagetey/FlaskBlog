from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
import jwt
from flask import current_app
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('Пароль не читается')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        generate_token = jwt.encode(
            {'confirm': self.id,
             'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)
             },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return generate_token

    def confirm(self, token):
        try:
            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                 leeway=datetime.timedelta(seconds=10),
                 algorithms=["HS256"]
            )
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        token_res = jwt.encode(
            {'reset': self.id,
             'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)
             },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return token_res

    def reset_password(self, token, new_password):
        try:
            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True