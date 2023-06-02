from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, session, request, redirect, url_for


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buyhere.db'
db = SQLAlchemy(app)


@app.route('/')
def home():
    return "Home page"


@app.route('/register')
def register():
    return render_template('admin/register.html', title="Register User")
