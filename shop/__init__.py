from shop.admin import routes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buyhere.db'
app.config['SECRET_KEY'] = 'secretkey_isse_jaguar'
db = SQLAlchemy(app)
