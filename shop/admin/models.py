from shop import app, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False,
                        nullable=False, default='profile.jpg')
    sell_count = db.Column(db.Integer, nullable=True, default=0)
    def __repr__(self):
        return '<User %r>' % self.username


with app.app_context():
    db.create_all()
