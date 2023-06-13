from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos, search, bcrypt
from .forms import CustomerRegisterForm
from .model import Register
import secrets
import os

@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data}! Thank you for registering 🎉', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customer/register.html', form=form)