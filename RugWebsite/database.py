from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, String

from RugWebsite.__init__ import db, meta, engine

def createAll():
    meta.create_all(engine)
def dropAll():
    meta.drop_all(engine, checkfirst=True)


# SQLAlchemy Tables
USERS_Table = Table("Users", meta,
                        Column("id", Integer, primary_key=True, autoincrement=True, nullable=True),
                        Column("username", String, unique=True, nullable=False),
                        Column("password", String, nullable=False),
                        Column("email", String, nullable=True)
                    )

# Python classes - Each class corresponds to one Table
class Users(db.Model, UserMixin):
    __tablename__ = "Users"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True, nullable=True, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(40), nullable=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"{self.username}"
