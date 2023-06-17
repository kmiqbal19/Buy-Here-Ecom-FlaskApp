from sqlalchemy import func
from shop import db, app
from datetime import datetime, timedelta, date


class Addproduct(db.Model):
    __searchable__ = ['name', 'desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    discount_expiration = db.Column(db.DateTime, nullable=True)
    previous_discounts = db.relationship('DiscountExpiredOffer', backref='product', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('categories', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image3.jpg')

    
    def __repr__(self):
        return '<Addproduct %r>' % self.name
    
    def is_discount_expired(self):
        if self.discount_expiration is not None:
            print(self.discount_expiration)
            current_date = datetime.today()  # Get the current date
            return self.discount_expiration.date() < current_date.date()
        return False

class DiscountExpiredOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discount_percentage = db.Column(db.Integer, nullable=False)
    discount_ended = db.Column(db.DateTime, nullable=False, default=func.now() - timedelta(days=1))
    product_name =  db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('addproduct.id'), nullable=False)

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


with app.app_context():
    db.create_all()
