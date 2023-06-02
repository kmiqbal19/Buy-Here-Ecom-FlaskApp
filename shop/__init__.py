from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, session, request, redirect, url_for, flash

from .admin.forms import RegistrationForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buyhere.db'
db = SQLAlchemy(app)

# ---- ROUTES ------


@app.route('/')
def home():
    return "Home page"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # user = User(form.username.data, form.email.data,
        #             form.password.data)
        # db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title="Registeration Page")
