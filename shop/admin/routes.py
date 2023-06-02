from shop import app

from flask import render_template, session, request, redirect, url_for


@app.route('/')
def home():
    return "Home page"


@app.route('/register')
def register():
    return render_template('admin/register.html', title="Register User")
