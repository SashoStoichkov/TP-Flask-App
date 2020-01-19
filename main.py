from flask import Flask
from flask import render_template, request, redirect, url_for

from user import User
from product import Product

app = Flask(__name__)


@app.route("/")
def index():
    products = Product.get_all_products()
    return render_template("index.html", products=products)


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
            request.form["price"]
        )

        if all(values[i] == "" for i in range(1, 4)):
            return redirect("/")

        Product(*values).add_product()
        return redirect("/")


@app.route("/products/<int:id>/delete/")
def delete_product(id):
    product = Product.find_product(id)

    product.delete_product()

    return redirect("/")


if __name__ == "__main__":
    app.run()
