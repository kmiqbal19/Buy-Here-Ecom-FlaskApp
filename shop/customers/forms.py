from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError, SelectField
from wtforms.validators import InputRequired
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from .model import Register

class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    zipcode = StringField('Zip code: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Image only please')])
    submit = SubmitField('Register')
    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")

class CustomerLoginFrom(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
    
class RatingForm(FlaskForm):
    rating = SelectField('Rating', choices=[('5', '5 stars'), ('4', '4 stars'), ('3', '3 stars'), ('2', '2 stars'), ('1', '1 star')], validators=[InputRequired()])
    review = TextAreaField('Review')
    submit = SubmitField('Submit')