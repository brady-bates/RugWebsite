import flask_login
from flask import redirect, url_for, flash, render_template, request
from flask_login import login_required, logout_user, login_user
from RugWebsite import app, ph
from RugWebsite.forms import LoginForm, RegisterForm

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
    return redirect(url_for("home"))

@app.route("/home")
def home():
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
