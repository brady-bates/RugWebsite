# TODO Add login system and page
# TODO Add SQL Alchemy Database
# TODO Add cart and products
# TODO Format HTML pages
# TODO Figure out purchase verification
# TODO Figure out security

from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify

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

