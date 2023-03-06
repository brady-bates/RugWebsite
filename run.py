# NOW
# TODO Add login system and page
# DONE Add SQL Alchemy Database
# TODO Add cart
#
# AFTER MEETING WITH ELIJAH
# TODO Add products
# TODO Format HTML pages
#
# END
# TODO Add email sending
# TODO Figure out security
# TODO Figure out purchase verification
# TODO Add to server
import flask_login
from flask import session, redirect, url_for, request, flash
from flask_login import login_required, logout_user, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from RugWebsite import app, db


engine = create_engine("sqlite:///database.db", echo=True)
Session = sessionmaker(engine)
session = Session()

login_manager = flask_login.LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

meta = MetaData()
USERS_Table = Table("Users", meta,
                    Column("id", Integer, primary_key=True, autoincrement=True, nullable=True),
                    Column("username", String, unique=True, nullable=False),
                    Column("password", String, nullable=False),
                    Column("email", String, nullable=True))
# TODO
# THIS LINE CLEARS DATABASE, REMEMBER TO REMOVE
meta.drop_all(engine, checkfirst=True)
meta.create_all(engine)

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

    # Python's toString()
    def __repr__(self):
        return f"{self.username}"


@login_manager.user_loader
def load_user(user_id):
    return session.query(Users).filter_by(id = user_id).first()

# session.query(Users).filter(Users.username.like("admin")).delete()
# test1 = Users(username="test1", password=ph.hash("password"))
# session.add(test1)
# session.commit()

# Specifies what to do if User is not logged in
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("You must be logged in")
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
