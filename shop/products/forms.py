from wtforms import Form, SubmitField, IntegerField, FloatField, StringField,DateField, TextAreaField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    discount_days = DateField('Discount Expiration', format='%Y-%m-%d')
    stock = IntegerField('Stock', [validators.DataRequired()])
    colors = StringField('Colors', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg, png, gif, jpeg'])])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg, png, gif, jpeg'])])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg, png, gif, jpeg'])])


class Message(Form):
    name = StringField('Your Name', [validators.DataRequired()])
    email = StringField('Your Email', [validators.DataRequired()])
    message = StringField('Message', [validators.DataRequired()])

class ProductRatingForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    review = TextAreaField('Review')
