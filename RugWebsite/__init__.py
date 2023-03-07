from flask import Flask
from argon2 import PasswordHasher
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

# Flask App Instantiation/Configuration
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "TOPSECRETKEY"

# Creating objects to be passed to other Classes
ph = PasswordHasher()
db = SQLAlchemy(app)
meta = MetaData()
engine = create_engine("sqlite:///database.db", echo=True)
Session = sessionmaker(engine)
session = Session()

from RugWebsite import routes
