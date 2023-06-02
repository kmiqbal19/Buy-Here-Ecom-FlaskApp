from flask import redirect, render_template, url_for, flash, request, session
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets

# ---- ROUTES ----


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brand')


@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getcat = request.form.get('category')
        cat = Category(name=getcat)
        db.session.add(cat)
        flash(f'The Category {getcat} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html')


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


@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
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
        addproduct = Addproduct(name=name, price=price, discount=discount, stock=stock,
                                colors=colors, desc=desc, category_id=category, brand_id=brand,
                                image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addproduct)
        flash(f'The product {name} was added in database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('products/addproduct.html', form=form, title='Add Product', brands=brands, categories=categories)
