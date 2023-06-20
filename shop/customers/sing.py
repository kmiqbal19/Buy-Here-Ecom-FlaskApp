# MODELS
class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('register.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)
    # Define the relationship with ProductRating
    product_ratings = db.relationship('ProductRating', backref='order', lazy=True)
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

# FORM
class RatingForm(FlaskForm):
    rating = SelectField('Rating', choices=[('5', '5 stars'), ('4', '4 stars'), ('3', '3 stars'), ('2', '2 stars'), ('1', '1 star')], validators=[InputRequired()])
    review = TextAreaField('Review')
    submit = SubmitField('Submit')
    
# ROUTE
@app.route('/rate_product/<invoice>/<product_id>', methods=['GET', 'POST'])
@login_required
def rate_product(invoice, product_id):
    order = CustomerOrder.query.filter_by(invoice=invoice, customer_id=current_user.id).first()
    if not order:
        flash('Invalid order or product.', 'danger')
        return redirect(url_for('home'))

    # Check if the product exists in the order
    product = order.orders.get(product_id)
    if not product:
        flash('Invalid product.', 'danger')
        return redirect(url_for('home'))

    form = RatingForm()
    if form.validate_on_submit():
        rating = form.rating.data
        review = form.review.data

        # Create a new ProductRating object
        product_rating = ProductRating(
            customer_order_id=order.id,
            product_id=product_id,
            rating=rating,
            review=review
        )
       
        # Save the product rating to the database
        db.session.add(product_rating)
        db.session.commit()

        flash('Thank you for rating the product!', 'success')
        return redirect(url_for('home'))

    return render_template('customer/thanks.html')

# HTML
<!-- Rating Form -->
            <hr>
            <h4>Rate this product:</h4>
            <form action="{{ url_for('rate_product' ,invoice=customer_order.invoice, product_id = product.id)}}" method="post">
                <input type="hidden" name="product_id" value="{{ product.id }}">
                <div class="form-group">
                    <label for="rating">Rating:</label>
                    <select class="form-control" name="rating" id="rating">
                        <option value="5">5 stars</option>
                        <option value="4">4 stars</option>
                        <option value="3">3 stars</option>
                        <option value="2">2 stars</option>
                        <option value="1">1 star</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="review">Review:</label>
                    <textarea class="form-control" name="review" id="review" rows="3"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Submit Rating</button>
            </form>