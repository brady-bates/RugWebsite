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
import json

import flask_login
from argon2 import PasswordHasher
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_login import login_required, logout_user, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "TOPSECRETKEY"
app.secret_key = "TOPSECRETKEY"
ph = PasswordHasher()

Base = declarative_base()
db = SQLAlchemy(app)
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


session.query(Users).filter(Users.username.like("admin")).delete()
test1 = Users(username="test1", password=ph.hash("password"))
session.add(test1)
session.commit()


@app.route("/")
def base():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    flash(ph.hash("fortnite"))
    flash(ph.hash("fortnite"))
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    entered_username = form.username.data

    if request.method == 'POST' and form.validate():
        stored_user = session.query(Users).filter_by(username=entered_username).first()
        entered_user_password = form.password.data

        if ph.verify(stored_user.password, entered_user_password):
            login_user(stored_user)
            flash("You are logged in", "info")
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('login'))

# Specifies what to do if User is not logged in
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("You must be logged in")
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        hashed_password = ph.hash(form.password.data)
        new_user = Users(username=form.username.data, password=hashed_password)
        print(new_user)
        session.add(new_user)
        session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/tables")
def tables():
    return render_template("tables.html")

@app.route("/rugs")
def rugs():
    return render_template("rugs.html")


@app.route("/edit")
@login_required
def edit():
    return render_template("edit.html")


@app.route("/user")
@login_required
def user():

    return render_template("user.html")

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
