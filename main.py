from flask import Flask
from flask import render_template, request, redirect,\
                  jsonify, session, url_for, flash, abort
from functools import wraps
import json

from user import User
from product import Product
from forms import RegistrationForm, LoginForm, ProductForm

app = Flask(__name__)


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verify_token(token):
            flash('You need to log in to do this!', 'danger')
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
@app.route('/products')
def index():
    products = Product.get_all_active_products()

    if (session):
        user = User.get_user_by_email(session["email"])
        user_id = User.get_id_by_email(session["email"])

        bought_products = Product.get_all_unactive_products(user_id)
        all_products = Product.get_all_products(user_id)

        return render_template(
            "index.html",
            products=products, bought_products=bought_products,
            username=user.name, all_products=all_products
        )

    else:
        return render_template(
            "index.html",
            products=products, username="GuestUser"
        )


@app.route("/products/new/", methods=["GET", "POST"])
@require_login
def create_product():
    form = ProductForm()

    if form.validate_on_submit():
        product = Product(
            id=None,
            title=form.title.data,
            content=form.content.data,
            price=form.price.data
        )

        product.add_product(User.get_id_by_email(session['email']))

        flash(f'{form.title.data} has been created!', 'success')
        return redirect(url_for('index'))

    return render_template(
        "product/edit_product.html",
        title="Create Product", form=form,
        legend="Add new product"
    )


@app.route("/products/<int:id>/")
def view_product(id):
    product = Product.find_product(id)
    auth = 1

    if product.get_publisher_id() != User.get_id_by_email(session["email"]):
        auth = 0

    return render_template(
        "product/product.html",
        title=product.title, product=product, auth=auth
    )


@app.route("/products/<int:id>/edit/", methods=["GET", "POST"])
@require_login
def edit_product(id):
    product = Product.find_product(id)

    form = ProductForm()

    if form.validate_on_submit():
        new_product = Product(
            id=product.id,
            title=form.title.data,
            content=form.content.data,
            price=form.price.data
        )

        product.edit_product(new_product)
        flash(f'{form.title.data} has been updated!', 'success')
        return redirect(url_for('view_product', id=product.id))

    elif request.method == "GET":
        form.title.data = product.title
        form.content.data = product.content
        form.price.data = product.price

    return render_template(
        "product/edit_product.html",
        title="Edit Product", form=form,
        legend="Edit product"
    )


@app.route("/products/<int:id>/delete/", methods=["POST"])
@require_login
def delete_product(id):
    product = Product.find_product(id)

    flash(f'{product.title} has been deleted!', 'success')
    product.delete_product()

    return redirect("/")


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            name=form.username.data,
            address=form.address.data,
            phone=form.phone.data
        )

        user.password = User.encrypt_password(form.password.data)
        user.create(User.encrypt_password(form.password.data))

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))

    return render_template('user/register.html', title='Register', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.get_user_by_email(email)
        if not user or not user.verify_password(password, email):
            flash('Check email or password!', 'danger')
            return jsonify({'token': None})

        session['email'] = user.email
        token = user.generate_token()

        flash('You have logged in successfully!', 'success')
        return jsonify({'token': token.decode('ascii')})

    return render_template('user/login.html', title='LogIn', form=form)


@app.route("/products/<int:product_id>/buy/")
@require_login
def buy_product(product_id):
    owner_id = User.get_id_by_email(session['email'])
    Product.buy_product(product_id, owner_id)

    product = Product.find_product(product_id)
    p_id = product.get_publisher_id()

    flash('Congratulations on your purchase!', 'success')
    flash(f'Contact {User.get_username_by_id(p_id)} to confirm!', 'success')
    return redirect("/")


@app.route("/profile/<string:username>/")
def profile(username):
    user = User.get_user_by_username(username)

    return render_template(
        'user/profile.html',
        title=username+"'s Profile", user=user
    )


if __name__ == '__main__':
    app.secret_key = 'i am very secret'
    app.config['SESSION_TYPE'] = 'shopSession'

    app.run(debug=True)
