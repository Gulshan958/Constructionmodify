from flask import Flask, render_template, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField,FloatField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from flask_bcrypt import Bcrypt
from flask_login import current_user, LoginManager, UserMixin, login_user, logout_user, login_required
from flask import request
from models import Supplier,db,Cart,Product,Order
from forms import SupplierLoginForm 
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from flask import jsonify
from datetime import datetime
import os,json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



from flask import send_from_directory

@app.route('/logo.avif')
def favicon():
    return send_from_directory('static/images', 'logo.avif', mimetype='image/vnd.microsoft.icon')

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

# Product Table
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    supplier = db.relationship('Supplier', backref=db.backref('products', lazy=True))

# cart Table
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    order_date = db.Column(db.DateTime, default=datetime.now)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)

    user = db.relationship('User', backref=db.backref('cart', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

    # Auto-update total amount
    def update_total_amount(self):
        product = Product.query.get(self.product_id)
        if product:
            self.total_amount = product.price * self.quantity

# order Table
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Ensure this exists
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)  # ✅ Add this column
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    # date_ordered = db.Column(db.DateTime, default=datetime.utcnow)
    
    date_ordered = db.Column(db.DateTime, default=datetime.now)
    product = db.relationship("Product", backref="orders")  # Relationship with Product
    address = db.relationship("Address", backref="orders")  # ✅ Relationship with Address

# Address Table
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    mobile_no = db.Column(db.BigInteger, unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.String(6), nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("User", backref=db.backref("addresses", lazy=True))


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id)) or db.session.get(Supplier, int(user_id))

# Customer Registration Form
class RegistrationForm(FlaskForm):
    userName= StringField('Username', validators=[DataRequired(),Length(min=3,max=8)])
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=70)])
    mobileNumber = IntegerField('Mobile Number', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    nearby_landmark = StringField('Nearby Landmark', validators=[Length(max=100)])
    village = StringField('Village', validators=[Length(max=100)])
    district = StringField('District', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Supplier Registration Form
class SupplierRegistrationForm(FlaskForm):
    userName= StringField('Username', validators=[DataRequired(),Length(min=3,max=8)])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=70)])
    mobileNumber = IntegerField('Mobile Number', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    shopName = StringField('Shop Name', validators=[DataRequired(), Length(max=100)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    nearby_landmark = StringField('Nearby Landmark', validators=[Length(max=100)])
    village = StringField('Village', validators=[Length(max=100)])
    district = StringField('District', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Login Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

#supplier login Forms
class SupplierLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Product Form
class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=100)])
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    description = StringField('Description', validators=[Length(max=255)])
    image = FileField('Product Image', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add Product')

# Edit Product Form
class EditProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = FloatField("Price ($)", validators=[DataRequired(), NumberRange(min=0)])
    description = StringField("Description", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
    image = FileField("Product Image")
    submit = SubmitField("Save Changes")

# Address Form
class AddressForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=3, max=100)])
    mobile_no = IntegerField('Mobile Number', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    address = StringField("Address", validators=[DataRequired(), Length(min=5, max=255)])
    city = StringField("City", validators=[DataRequired(), Length(min=2, max=100)])
    state = StringField("State", validators=[DataRequired(), Length(min=2, max=100)])
    pin_code = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField("Save Address")


@app.route('/')
def home():
    return render_template('home.html', current_user=current_user)


# Customer or user login
@app.route('/login', methods=['GET', 'POST'])  # ✅ Ensure both GET and POST are allowed
def login():
    form = LoginForm()  # Initialize form

    if request.method == "POST":  # ✅ Ensure request is POST
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return jsonify({"success": True, "message": "Login successful!", "redirect_url": url_for('home')})
        
        return jsonify({"success": False, "message": "Invalid email or password. Please try again."})

    return render_template("login.html", form=form)  # ✅ Ensure GET request renders login page


# Supplier login
@app.route('/supplier_login', methods=['GET', 'POST'])
def supplier_login():
    form = SupplierLoginForm()
    
    if request.method == "POST":
        form = SupplierLoginForm(request.form)
        if form.validate():
            supplier = Supplier.query.filter_by(email=form.email.data).first()
            if supplier and bcrypt.check_password_hash(supplier.password, form.password.data):
                login_user(supplier)
                return jsonify({"success": True, "message": "Login successful!", "redirect_url": url_for('home')})
        
        return jsonify({"success": False, "message": "Invalid email or password. Please try again."})

    return render_template("supplier_login.html", form=form)


# add product route
@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not isinstance(current_user, Supplier):  # Check if logged-in user is a Supplier
        flash("Only suppliers can add products!", "danger")
        return redirect(url_for('shop'))

    form = ProductForm()
    if form.validate_on_submit():
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_path = os.path.join('static/uploads', filename)
                os.makedirs('static/uploads', exist_ok=True)  # Ensure upload folder exists
                image_file.save(image_path)

                product = Product(
                    name=form.name.data,
                    price=form.price.data,
                    quantity=form.quantity.data,
                    description=form.description.data,
                    image=filename,
                    supplier_id=current_user.id
                )
                db.session.add(product)
                db.session.commit()
                flash('Product added successfully!', 'success')
                return redirect(url_for('shop'))
            else:
                flash('Please upload an image.', 'danger')
    return render_template('add_product.html', form=form)

# Shop
@app.route('/shop')
@login_required
def shop():
    search_query = request.args.get('search', '').strip()
    
    if isinstance(current_user, Supplier):
        products_query = Product.query.filter_by(supplier_id=current_user.id)
    else:
        products_query = Product.query

    # Apply search filter
    products = products_query.filter(Product.name.ilike(f"%{search_query}%")).all() if search_query else products_query.all()

    return render_template('shop.html', products=products, search_query=search_query, product_not_found=bool(search_query and not products))


#Edit Product 
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Ensure only the supplier who added the product can edit it
    if current_user.__class__.__name__ != 'Supplier' or product.supplier_id != current_user.id:
        flash("You do not have permission to edit this product.", "danger")
        return redirect(url_for('shop'))

    form = EditProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        product.quantity = form.quantity.data
        if form.image.data:
            # Save and update image (implement image saving logic)
            pass
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('shop'))

    return render_template('edit_product.html', form=form, product=product)

# add to cart

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        return jsonify({"success": False, "message": "Login required to add items to cart!", "redirect": url_for('login')})

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found."})

    existing_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_item:
        return jsonify({"success": False, "message": "Item is already in the cart!"})

    cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=1)
    db.session.add(cart_item)
    db.session.commit()

    return jsonify({"success": True, "message": "Item added to cart!"})



# Cart Route
@app.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    
    # Calculate total cart amount
    total_cart_amount = sum(item.quantity * item.product.price for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total_cart_amount=total_cart_amount)

# quantity update
@app.route('/update_quantity/<int:cart_id>/<action>', methods=['POST'])
@login_required
def update_quantity(cart_id, action):
    # cart_item = Cart.query.get(cart_id)
    cart_item = db.session.get(Cart, cart_id)


    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404

    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Item removed from cart'})

    cart_item.total_amount = cart_item.quantity * cart_item.product.price
    db.session.commit()

    # Recalculate total cart amount
    total_cart_amount = sum(item.quantity * item.product.price for item in Cart.query.filter_by(user_id=current_user.id).all())

    return jsonify({'success': True, 'total_cart_amount': total_cart_amount})

# update cart
@app.route('/update_cart', methods=['POST'])  # Separate route for updates
@login_required
def update_cart():
    # Code to update cart
    return jsonify({'success': True})

# Checkout Route
@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        return jsonify({"success": False, "error": "Your cart is empty!"})

    # ✅ Store order details in session but do NOT clear the cart
    order_details = []
    for item in cart_items:
        order_details.append({
            "product_id": item.product.id,
            "product_name": item.product.name,
            "image": item.product.image,
            "price": item.product.price,
            "quantity": item.quantity,
            "total_price": item.product.price * item.quantity
        })

    session["order_details"] = order_details  # ✅ Store order in session
   

    return jsonify({"success": True, "redirect_url": url_for('shipping')})


# Shipping Route
@app.route('/shipping', methods=['GET', 'POST'])
@login_required
def shipping():
    form = AddressForm()

    if form.validate_on_submit():
        new_address = Address(
            user_id=current_user.id,
            full_name=form.full_name.data,
            mobile_no=form.mobile_no.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            pin_code=form.pin_code.data
        )
        db.session.add(new_address)
        db.session.commit()
        flash("New address saved successfully!", "success")
        return redirect(url_for('shipping'))

    addresses = Address.query.filter_by(user_id=current_user.id).all()
    return render_template("shipping.html", form=form, addresses=addresses)

# Customer Signup  
@app.route('/signup', methods=['GET', 'POST'])  # ✅ Ensure both methods are allowed
def signup():
    form = RegistrationForm()
    
    if request.method == "POST" and form.validate_on_submit():
        email_exists = User.query.filter_by(email=form.email.data).first()
        mobile_exists = User.query.filter_by(mobileNumber=form.mobileNumber.data).first()

        if email_exists:
            return jsonify({"success": False, "message": "Email is already registered!."})

        if mobile_exists:
            return jsonify({"success": False, "message": "Mobile number is already registered!"})

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        new_user = User(
            userName=form.userName.data,
            name=form.name.data,
            email=form.email.data,
            mobileNumber=form.mobileNumber.data,
            pincode=form.pincode.data,
            nearby_landmark=form.nearby_landmark.data,
            village=form.village.data,
            district=form.district.data,
            state=form.state.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": True, "message": "Signup successful!", "redirect_url": url_for('login')})

    return render_template('signup.html', form=form)




# Supplier Signup
@app.route('/supplier_signup', methods=['GET', 'POST'])
def supplier_signup():
    form = SupplierRegistrationForm()

    if request.method == "POST" and form.validate_on_submit():
        email_exists = Supplier.query.filter_by(email=form.email.data).first()
        mobile_exists = Supplier.query.filter_by(mobileNumber=form.mobileNumber.data).first()

        if email_exists:
            return jsonify({"success": False, "message": "Email is already registered!"})

        if mobile_exists:
            return jsonify({"success": False, "message": "Mobile number is already registered!"})

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        new_supplier = Supplier(
            userName=form.userName.data,
            name=form.name.data,
            email=form.email.data,
            mobileNumber=form.mobileNumber.data,
            shopName=form.shopName.data,
            pincode=form.pincode.data,
            nearby_landmark=form.nearby_landmark.data,
            village=form.village.data,
            district=form.district.data,
            state=form.state.data,
            password=hashed_password
        )

        db.session.add(new_supplier)
        db.session.commit()

        return jsonify({"success": True, "message": "Supplier account created successfully!", "redirect_url": url_for('supplier_login')})

    return render_template('supplier_signup.html', form=form)

# Payment Route
@app.route("/payment")
@login_required
def payment():
    return render_template("payment.html")

# user confirm order
@app.route("/confirm-order", methods=["POST"])
@login_required
def confirm_order():
    if "order_details" not in session:
        return jsonify({"success": False, "error": "No orders to confirm."})

    order_details = session.pop("order_details", [])

    if not order_details:
        return jsonify({"success": False, "error": "Your cart is empty!"})

    # ✅ Fetch user's saved address
    address = Address.query.filter_by(user_id=current_user.id).first()
    if not address:
        return jsonify({"success": False, "error": "No saved shipping address found."})

    for item in order_details:
        order = Order(
            user_id=current_user.id,
            product_id=item["product_id"],
            address_id=address.id,  # ✅ Must not be None
            quantity=item["quantity"],
            total_price=item["total_price"],
            status="Pending",
            date_ordered=datetime.now()
        )
        db.session.add(order)

    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return jsonify({"success": True, "redirect_url": url_for('orders')})


# supplier confirm the order when deliver
@app.route('/confirm_order/<int:order_id>', methods=['POST'])
@login_required
def supplier_confirm_order(order_id):
    if not isinstance(current_user, Supplier):
        return jsonify({"success": False, "error": "Only suppliers can confirm orders!"})

    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"success": False, "error": "Order not found!"})

    if order.product.supplier_id != current_user.id:
        return jsonify({"success": False, "error": "You cannot confirm this order!"})

    order.status = "Confirmed"
    db.session.commit()

    return jsonify({"success": True, "message": "Order has been confirmed!"})

# Supplier Orders
@app.route('/supplier_orders')
@login_required
def supplier_orders():
    if not isinstance(current_user, Supplier):
        flash("Only suppliers can view orders!", "danger")
        return redirect(url_for('home'))

    # Fetch orders with user and address details
    orders = (
        db.session.query(Order, User, Address)
        .join(Product, Order.product_id == Product.id)
        .join(User, Order.user_id == User.id)
        .join(Address, Order.address_id == Address.id)  # ✅ Join Address table
        .filter(Product.supplier_id == current_user.id)
        .all()
    )

    return render_template('supplier_orders.html', orders=orders)


# orders route
@app.route("/orders")
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()  # Fetch full order objects
    return render_template("orders.html", orders=orders)

#Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# main
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)




 