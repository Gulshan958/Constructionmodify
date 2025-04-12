from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
db = SQLAlchemy()


# Customer Table
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    mobileNumber = db.Column(db.BigInteger, unique=True, nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    nearby_landmark = db.Column(db.String(100), nullable=True)
    village = db.Column(db.String(100), nullable=True)
    district = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)

       # Relationship to Address (One-to-Many)
    addresses = db.relationship('Address', backref='user', lazy=True)

    # Relationship to Orders
    orders = db.relationship('Order', backref='customer', lazy=True)

# Supplier Table
class Supplier(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    nearby_landmark = db.Column(db.String(100), nullable=True)
    village = db.Column(db.String(100), nullable=True)
    district = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    mobileNumber = db.Column(db.BigInteger, unique=True, nullable=False)
    shopName = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)

        # Relationship to Products
    products = db.relationship('Product', backref='supplier', lazy=True)




# Product Table
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)  # Image filename
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)

    supplier = db.relationship('Supplier', backref=db.backref('products', lazy=True))
        # Relationship to Orders
    orders = db.relationship('Order', backref='product', lazy=True)

# Cart Model
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image = db.Column(db.String(200), nullable=True)  # Image filename
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    order_date = db.Column(db.DateTime, default=datetime.now)

    total_amount = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref=db.backref('cart', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

    def update_total(self):
        self.total_amount = self.quantity * self.product.price


# order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Ensure this exists
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)  # ✅ Add this column

    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    date_ordered = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship('User', backref=db.backref('cart', lazy=True))

    product = db.relationship("Product", backref="orders")  # Relationship with Product
    address = db.relationship("Address", backref="orders")  # ✅ Relationship with Address


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    mobile_no= db.Column(db.BigInteger, unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


    user = db.relationship('User', backref=db.backref('addresses', lazy=True))
