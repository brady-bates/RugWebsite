import flask_login
from flask import redirect, url_for, flash, render_template, request
from flask_login import login_required, logout_user, login_user
from RugWebsite import app, ph
from RugWebsite.forms import LoginForm, RegisterForm
from argon2.exceptions import VerifyMismatchError

from run import Users, session

login_manager = flask_login.LoginManager(app)
login_manager.init_app(app)
@login_manager.user_loader                   # Necessary for Flask Login to work
def load_user(user_id):
    return session.query(Users).filter_by(id = user_id).first()

@login_manager.unauthorized_handler          # Specifies what to do if User is not logged in
def unauthorized_callback():
    flash("You must be logged in")
    return redirect(url_for('login'))

@app.route("/")
def base():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate():
        stored_user = session.query(Users).filter_by(username=form.username.data).first()

        try:
            if ph.verify(stored_user.password, form.password.data):
                login_user(stored_user)
                flash("You are logged in", "info")
                ph.check_needs_rehash(stored_user.password)

        except VerifyMismatchError:
            flash("You have entered the incorrect password")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    # If Request type is Post and the form validates
    if request.method == 'POST' and form.validate():
        # If there is not an existing user
        if session.query(Users).filter_by(username=form.username.data).count() == 0:
            new_user = Users(username=form.username.data, password=ph.hash(form.password.data))
            print(new_user)
            session.add(new_user)
            session.commit()
        else:
            flash("This Username already exists, try a different username")
            return redirect(url_for("register"))
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
