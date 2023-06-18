import json
from shop import app, db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)
# Customer
class Register(db.Model, UserMixin):
    __tablename__ = 'register'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), unique= False)
    f_name = db.Column(db.String(50), unique= False)
    username = db.Column(db.String(50), unique= True)
    email = db.Column(db.String(50), unique= True)
    password = db.Column(db.String(200), unique= False)
    country = db.Column(db.String(50), unique= False)
    # state = db.Column(db.String(50), unique= False)
    city = db.Column(db.String(50), unique= False)
    contact = db.Column(db.String(50), unique= False)
    address = db.Column(db.String(50), unique= False)
    zipcode = db.Column(db.String(50), unique= False)
    profile = db.Column(db.String(200), unique= False , default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Define the relationship with CustomerOrder
    orders = db.relationship('CustomerOrder', backref='customer', lazy=True)
    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self): 
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    
    def __repr__(self):
        return '<Register %r>' % self.name

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('register.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)
    # Define the relationship with ProductRating
    product_ratings = db.relationship('ProductRating', backref='customer_order', lazy=True)
    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice

class ProductRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_order_id = db.Column(db.Integer, db.ForeignKey('customer_order.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<ProductRating %r>' % self.id

with app.app_context():
    db.create_all()