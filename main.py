from flask import Flask
from flask import render_template, request, redirect, jsonify
from functools import wraps
import json

from user import User
from product import Product

app = Flask(__name__)


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verify_token(token):
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
def index():
    products = Product.get_all_products()
    return render_template("index.html", products=products)


@app.route("/products/")
def list_products():
    products = Product.get_all_products()
    return render_template("product/products.html", products=products)


@app.route("/products/new/", methods=["GET", "POST"])
@require_login
def create_product():
    if request.method == "GET":
        return render_template("product/new_product.html")
    elif request.method == "POST":
        values = (
            None,
            request.form["title"],
            request.form["content"],
            request.form["price"]
        )

        if all(values[i] == "" for i in range(1, 4)):
            return redirect("/")

        Product(*values).add_product()
        return redirect("/")


@app.route("/products/<int:id>/edit/", methods=["GET", "POST"])
@require_login
def edit_product(id):
    product = Product.find_product(id)

    if request.method == "GET":
        return render_template(
            "product/edit_product.html", id=id, product=product
        )
    elif request.method == "POST":
        v = (
            product.id,
            request.form["title"],
            request.form["content"],
            request.form["price"]
        )

        product.edit_product(Product(*v))
        return redirect("/")


@app.route("/products/<int:id>/delete/")
@require_login
def delete_product(id):
    product = Product.find_product(id)

    product.delete_product()

    return redirect("/")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        values = (
            request.form['email'],
            request.form['username'],
            request.form['address'],
            request.form['phone']
        )

        if User.get_user_by_email(values[0]):
            return redirect('/register')
        user = User(*values)
        user.create(User.encrypt_password(request.form['password']))

        return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = json.loads(request.data.decode('ascii'))
        email = data['email']
        password = data['password']
        # from pdb import set_trace
        # set_trace()
        user = User.get_user_by_email(email)
        if not user or not user.verify_password(password):
            return jsonify({'token': None})
        token = user.generate_token()
        print("SUCCESS")
        return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    app.run()
