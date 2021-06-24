from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


# The base class which our objects will be defined on.
Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    username = Column(String(32), unique=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
