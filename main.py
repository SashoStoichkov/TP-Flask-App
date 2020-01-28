from flask import Flask
from flask import render_template, request, redirect, jsonify, session
from functools import wraps
import json

from user import User
from product import Product

app = Flask(__name__)
# sess = Session()


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
def list_products(email):
    print("I WAS CALLED_---------------------------------------------_-")
    products = Product.get_all_products()
    # user = User.get_user_by_email(email)
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
        user.password = User.encrypt_password(request.form['password'])
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
        user = User.get_user_by_email(email)
        if not user or not user.verify_password(password, email):
            return jsonify({'token': None})

        session['email'] = user.email
        token = user.generate_token()
        return jsonify({'token': token.decode('ascii')})


@app.route("/products/<int:prod_id>/buy/", methods=["GET", "POST"])
@require_login
def buy_product(prod_id):
    if request.method == "GET":
        from pdb import set_trace
        set_trace()
        return 'ok'
    if request.method == "POST":
        from pdb import set_trace
        set_trace()
        return redirect("/")


if __name__ == '__main__':
    app.secret_key = 'i am very secret'
    app.config['SESSION_TYPE'] = 'shopSession'

    app.run()
