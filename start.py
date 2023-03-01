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
from argon2 import PasswordHasher
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_login import login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "TOPSECRETKEY"
app.secret_key = "TOPSECRETKEY"

Base = declarative_base()
db = SQLAlchemy(app)
engine = create_engine("sqlite:///database.db", echo=True)
Session = sessionmaker(engine)
session = Session()

login = flask_login.LoginManager(app)
login.init_app(app)

ph = PasswordHasher()

meta = MetaData()
USERS_Table = Table("Users", meta, Column("id", Integer, primary_key=True, autoincrement=True, nullable=True),
                   Column("username", String, unique=True, nullable=False),
                   Column("password", String, nullable=False),
                   Column("email", String, nullable=True),
                   Column("salt", String, nullable=True)
                   )
# TODO
# THIS LINE CLEARS DATABASE, REMEMBER TO REMOVE
meta.drop_all(engine, checkfirst=True)

meta.create_all(engine)


class User(db.Model, flask_login.UserMixin):
    __tablename__ = "Users"
    id       = db.Column(db.Integer, primary_key=True, nullable=True, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    email    = db.Column(db.String(40), nullable=True)
    salt     = db.Column(db.String(20), nullable=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Python's toString()
    def __repr__(self):
        return f"{self.username}"

    def get_id(self):
        return id

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


session.query(User).filter(User.username.like("admin")).delete()
admin = User(username="admin", password="adminpass")
test1 = User(username="test1", password=ph.hash("testpassword"))
session.add(admin)
session.add(test1)
session.commit()

hash = ph.hash("correct horse battery staple")

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
        stored_user = session.query(User).filter(User.username==entered_username).first()
        flash(stored_user.password)
        entered_user_password = form.password.data

        if ph.verify(stored_user.password, entered_user_password):
            flask_login.login_user(User)
            flash("You are logged in", "info")
        else:
            flash("Login failed")

    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        hashed_password = ph.hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
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

@login_required
@app.route("/edit")
def edit():
    return render_template("edit.html")

@login_required
@app.route("/user")
def user():
    return render_template("user.html")

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect("somewhere")


session.commit()
if __name__ == "__main__":
    app.run(debug=True)
