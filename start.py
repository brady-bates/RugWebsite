# NOW
# TODO Add login system and page
# TODO Add SQL Alchemy Database
# TODO Add cart
# TODO Add more necessary flask packages
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

from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_login import login_manager
# from flask_sqlalchemy
# from flask_mailpp


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route("/tables")
def tables():
    return render_template("tables.html")


@app.route("/rugs")
def rugs():
    return render_template("rugs.html")


if __name__ == "__main__":
    app.run(debug=True)

