from flask import Flask
from flask import render_template, request, redirect  # , url_for
from user import User
from product import Product

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products/")
def list_products():
    products = Product.get_all_products()
    return render_template("product/products.html", products=products)


@app.route("/products/new/", methods=["GET", "POST"])
def create_product():
    if request.method == "GET":
        return render_template("product/new_product.html")
    elif request.method == "POST":
        values = (
            None,
            request.form["title"],
            request.form["content"],
            request.form["price"],
            None,
            None,
            None
        )

        Product(*values).add_product()
        return redirect("/")


@app.route("/products/<int:id>/delete/")
def delete_product(id):
    product = Product.find_product(id)

    product.delete_product()

    return redirect("/products/")


# TODO: Have to find a way to get current user's ID (in order to set
# it in the db - owner_id)``
@app.route("/products/<int:prod_id>/buy/<int:own_id>", methods=["GET", "POST"])
def buy_producit(prod_id, own_id):
    Product.buy_product(prod_id, own_id)
    return redirect("/")


@app.route("/register/", methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            request.form['email'],
            request.form['username'],
            request.form['address'],
            request.form['phone'],

        )
        User(*values).create(User.encrypt_password(request.form['password']))

        return redirect('/')


@app.route("/login/", methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        pass


if __name__ == "__main__":
    app.run()
