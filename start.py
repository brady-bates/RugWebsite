# NOW
# TODO Add login system and page
# TODO Add SQL Alchemy Database
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
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "TOPSECRETKEY"
app.secret_key = "TOPSECRETKEY"

Base = declarative_base()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model, UserMixin):
    __tablename__ = "Users"
    id       = db.Column(db.Integer, primary_key=True, nullable=True, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    email    = db.Column(db.String(40), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Python's toString()
    def __repr__(self):
        return f"{self.username}"


engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(engine)
session = Session()

session.query(User).where(User.username.like("admin")).delete()
admin = User(username="admin", password="adminpass")
session.add(admin)
session.commit()


@app.route("/")
def base():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
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
