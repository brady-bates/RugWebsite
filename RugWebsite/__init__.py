from flask import Flask
from argon2 import PasswordHasher
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "TOPSECRETKEY"
app.secret_key = "TOPSECRETKEY"

ph = PasswordHasher()

db = SQLAlchemy(app)

from RugWebsite import routes
