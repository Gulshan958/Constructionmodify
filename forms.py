from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed

#  1. User Registration Form
class RegistrationForm(FlaskForm):
    userName = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=70)])
    mobileNumber = IntegerField('Mobile Number', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    nearby_landmark = StringField('Nearby Landmark', validators=[Length(max=100)])
    village = StringField('Village', validators=[Length(max=100)])
    district = StringField('District', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

#  2. Supplier Registration Form
class SupplierRegistrationForm(FlaskForm):
    userName = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=70)])
    mobileNumber = IntegerField('Mobile Number', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    companyName = StringField('Company Name', validators=[DataRequired(), Length(max=100)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    nearby_landmark = StringField('Nearby Landmark', validators=[Length(max=100)])
    village = StringField('Village', validators=[Length(max=100)])
    district = StringField('District', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

#  3. User & Supplier Login Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SupplierLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

#  4. Product Form (Suppliers can add products)
class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=100)])
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=255)])
    image = FileField('Product Image', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add Product')

#  5. Edit Product Form (Suppliers can update products)
class EditProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = FloatField("Price ($)", validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField("Description", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
    image = FileField("Update Product Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Save Changes")

#  6. Cart Update Form
class UpdateCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Update Cart')

#  7. Order Confirmation Form (Supplier Confirms Order)
class ConfirmOrderForm(FlaskForm):
    submit = SubmitField("Confirm Order")

#  8. Shipping Address Form
class AddressForm(FlaskForm):
    fullName = StringField("Full Name", validators=[DataRequired(), Length(max=100)])
    mobile_no = IntegerField('Mobile Number', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    address = StringField("Address", validators=[DataRequired(), Length(max=255)])
    city = StringField("City", validators=[DataRequired(), Length(max=100)])
    state = StringField("State", validators=[DataRequired(), Length(max=100)])
    pin_code = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField("Save Address & Proceed")
