import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    username = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    stat_lvl_1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    stat_lvl_2 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    stat_lvl_3 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    total_lvl_1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    total_lvl_2 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    total_lvl_3 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)