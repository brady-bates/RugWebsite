from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def home(): 
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)