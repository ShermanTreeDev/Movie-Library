from time import time
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as so
import jwt
from main import app, db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    movies: so.WriteOnlyMapped['Movie'] = so.relationship(back_populates='add_user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return db.session.get(User, id)


"""
The user loader is registered with Flask-Login with the @login.user_loader decorator.
The id that Flask-Login passes to the function as an argument is going to be a string,
so databases that use numeric IDs need to convert the string to integer
"""


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Movie(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(140))
    add_user: so.Mapped[User] = so.relationship(back_populates='movies')

    def __repr__(self):
        return '<Post {}>'.format(self.title)
