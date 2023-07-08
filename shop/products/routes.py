from datetime import datetime
from flask import redirect, render_template, url_for, flash, request, session, current_app
from flask_login import current_user
from sqlalchemy import func, text
from shop import db, app, photos
from .models import Brand, Category, Addproduct, DiscountExpiredOffer, Messagea , ProductRating
from shop.customers.model import Register
from shop.admin.models import User
from .forms import Addproducts, Message, ProductRatingForm
import secrets
import os
# ---- ROUTES ----


def brands():
    brands = Brand.query.join(
        Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands


def categories():
    categories = Category.query.join(
        Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories

@app.route('/contactseller', methods=['GET', 'POST'])
def contactseller():
    form = Message(request.form)
    if request.method == 'POST':
        name = form.name.data
        email = form.email.data
        message_text = form.message.data

        message = Messagea(name=name, email=email, message=message_text)
        db.session.add(message)
        db.session.commit()
        flash('Your message has sent successfully! We will soon contact you. ')
        return redirect (url_for('products'))

    
    return render_template('products/contact_seller.html', form=form)


@app.route('/products')
def products():
    current_date = datetime.today()
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=1)
    return render_template('products/products.html', products=products, brands=brands(), categories=categories(), current_date=current_date)


@app.route('/dicountedproducts')
def discount_products():
    products = Addproduct.query.filter(Addproduct.discount > 0)
    previous_discounts = DiscountExpiredOffer.query.all()
    current_date = datetime.today()
    if products is None:
        redirect(url_for('products'))
        flash(f'There are no products with discount!')
    return render_template('products/discountedProducts.html', products=products, brands=brands(), categories=categories(), previous_discounts=previous_discounts, current_date=current_date)

@app.route('/dicountedEndproducts')
def discount_end_products():
    products = Addproduct.query.filter(Addproduct.discount > 0)
    previous_discounts = DiscountExpiredOffer.query.all()
    current_date = datetime.today()
    if products is None:
        redirect(url_for('products'))
        flash(f'There are no products with discount!')
    return render_template('products/discountedEndProducts.html', products=products, brands=brands(), categories=categories(), previous_discounts=previous_discounts, current_date=current_date)


@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(
        searchword, fields=['name', 'desc'], limit=6)
    return render_template('products/result.html', products=products)


@app.route('/product/<int:id>')
def single_page(id):
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
    
    ratings = list(ProductRating.query.join(Addproduct, (ProductRating.product_id == id)))
    product = Addproduct.query.get_or_404(id)
    
    rating_sum = sum(rating.rating for rating in ratings)
    rating_avg = round(rating_sum / len(ratings), 2) if ratings else 0
    
    discount_expired = product.is_discount_expired()
    
    return render_template('products/single_page.html', product=product, brands=brands(), categories=categories(), discount_expired=discount_expired, invoice=invoice, ratings=ratings, ratingAvg=rating_avg)



@app.route('/brand/<int:id>')
def get_brand(id):
    brand = Addproduct.query.filter_by(brand_id=id)
    current_date = datetime.today()
    return render_template('products/index.html', brand=brand, brands=brands(), categories=categories(), current_date=current_date)


@app.route('/categories/<int:id>')
def get_category(id):
    get_cat_prod = Addproduct.query.filter_by(category_id=id)
    current_date = datetime.today()
    return render_template('products/index.html', get_cat_prod=get_cat_prod, categories=categories(), brands=brands(), current_date=current_date)


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    admin_there = True
    if 'email' not in session:
        admin_there = False
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/addbrand.html', brands='brand' , admin_there=admin_there)


@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Login first please', 'danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(
            f'The brand {updatebrand.name} was changed to {brand}', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('products/updatebrand.html', title='Update brand', brands='brands', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        flash(
            f"The brand {brand.name} was deleted from your database", "success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(
        f"The brand {brand.name} can't be  deleted from your database", "warning")
    return redirect(url_for('admin'))


@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    admin_there = True
    if 'email' not in session:
        admin_there = False
        flash(f'Please login first', 'danger')
    if request.method == "POST":
        getcat = request.form.get('category')
        cat = Category(name=getcat)
        db.session.add(cat)
        flash(f'The Category {getcat} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', admin_there=admin_there)


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Login first please', 'danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecat.name = category
        flash(f'The category is changed to {category}', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('products/updatebrand.html', title='Update Category Page', updatecat=updatecat)


@app.route('/deletecat/<int:id>', methods=['GET', 'POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        flash(
            f"The brand {category.name} was deleted from your database", "success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(
        f"The brand {category.name} can't be  deleted from your database", "warning")
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    admin_there = True
    if 'email' not in session:
        admin_there = False
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    seller_email = session['email']
    seller_id = User.query.filter(User.email == seller_email).first().id
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        discount_days = form.discount_days.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get(
            'image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get(
            'image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get(
            'image_3'), name=secrets.token_hex(10) + ".")

        if discount_days != None:
            discount_expiration = discount_days

        product = Addproduct(name=name, price=price, discount=discount, stock=stock,
                             colors=colors, desc=desc, category_id=category, brand_id=brand,
                             image_1=image_1, image_2=image_2, image_3=image_3, discount_expiration=discount_expiration, seller_id=seller_id)
        db.session.add(product)
        db.session.commit()
        if product.is_discount_expired():
            product = Addproduct.query.filter_by(name=name).first()
            previous_discount = DiscountExpiredOffer(
                discount_percentage=product.discount, discount_ended=product.discount_expiration, product_name=product.name, product_id=product.id)
            db.session.add(previous_discount)
            db.session.commit()
        db.session.add(product)
        flash(f'The product {name} was added in the database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('products/addproduct.html', form=form, title='Add Product', brands=brands, categories=categories, admin_there=admin_there)


@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.desc = form.description.data
        product.category_id = category
        product.brand_id = brand
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get(
                    'image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get(
                    'image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get(
                    'image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get(
                    'image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get(
                    'image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get(
                    'image_3'), name=secrets.token_hex(10) + ".")

        flash('The product was updated', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.desc
    brand = product.brand.name
    category = product.category.name
    return render_template('products/updateproduct.html', form=form, title='Update Product', getproduct=product, brands=brands, categories=categories)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(
            f'The product {product.name} was delete from your record', 'success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product', 'success')
    return redirect(url_for('admin'))

@app.route('/rate_product/<int:product_id>/<customer_name>', methods=['GET', 'POST'])
def rate_product(product_id, customer_name):
    form = ProductRatingForm()
    if request.method == 'POST':
        rating = ProductRating(rating=form.rating.data, review=form.review.data, product_id=product_id,  customer_name=customer_name)
        db.session.add(rating)
        db.session.commit()
        return render_template('customer/thanks.html')
