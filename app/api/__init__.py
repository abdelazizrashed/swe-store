
from flask import Flask, redirect, request, session

from ..logic.modules.auth.services import AuthServices
from ..logic.modules.cart.services import CartServices
from ..logic.modules.product.services import ProductServices
from ..logic.utilities import Utilities


def register_routes(app: Flask):

    @app.route('/api/cart/add', methods=['GET'])
    def add_to_cart_api():
        amount = request.args.get('amount')
        id = request.args.get('id')
        try:
            amount = int(amount)
        except:
            return Utilities.response("Amount must be a number", status=400, success=False)
        if amount is None or id is None:
            return Utilities.response("Missing parameters", status=400, success=False)
        cart, products = CartServices.add_to_cart(
            session["user_id"], id, amount)
        return Utilities.response("Add to cart success", status=201, data={
            "cart": cart.to_dict(),
            "products": [product.to_dict() for product in products]
        })

    @app.route('/api/cart/empty', methods=['GET'])
    def empty_cart_api():
        cart, products = CartServices.empty_cart(session["user_id"])
        return Utilities.response("Empty cart success", status=201, data={
            "cart": cart.to_dict(),
            "products": [product.to_dict() for product in products]
        })

    @app.route('/api/cart/remove', methods=['GET'])
    def remove_from_cart_api():
        id = request.args.get('id')
        cart, products = CartServices.remove_product(session["user_id"], id)
        return Utilities.response("Remove from cart success", status=201, data={
            "cart": cart.to_dict(),
            "products": [product.to_dict() for product in products]
        })

    @app.route('/api/cart/remove-one', methods=['GET'])
    def remove_one_from_cart_api():
        id = request.args.get('id')
        cart, products = CartServices.remove_amount(
            session["user_id"], id, amount=1)
        return Utilities.response("Remove one from cart success", status=201, data={
            "cart": cart.to_dict(),
            "products": [product.to_dict() for product in products]
        })

    @app.route('/api/login', methods=['GET'])
    def login_api():
        email = request.args.get('email')
        password = request.args.get('password')
        if email is None or password is None:
            return Utilities.response("Missing parameters", status=400, success=False)
        try:
            user = AuthServices.login(email, password)
        except Exception as e:
            return Utilities.response(str(e), status=400, success=False)
        session['user_id'] = user.id
        session['email'] = user.email
        return Utilities.response("Login success", status=200, data=user.to_dict())

    @app.route('/api/register', methods=['GET'])
    def register_api():
        email = request.args.get('email')
        password = request.args.get('password')
        name = request.args.get('name')
        if email is None or password is None or name is None:
            return Utilities.response("Missing parameters", status=400, success=False)
        try:
            user = AuthServices.create_user(email, password, name)
        except Exception as e:
            return Utilities.response(str(e), status=400, success=False)
        return Utilities.response("Register success", status=201, data=user.to_dict())

    @app.route('/api/logout', methods=['GET'])
    def logout_api():
        session.clear()
        return Utilities.response("Logout success", status=200, success=True)

    @app.route('/api/product/create', methods=['POST'])
    def create_product_api():
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')

        url = Utilities.upload_img_from_file(
            request.files['image'], db_path="products")
        try:
            price = float(price)
        except:
            return Utilities.response("Price must be a number", status=400, success=False)
        if name is None or price is None or description is None:
            return Utilities.response("Missing parameters", status=400, success=False)
        try:
            product = ProductServices.create_product(
                name, description, url, price, "test")
        except Exception as e:
            return Utilities.response(str(e), status=400, success=False)
        return redirect('/dashboard')

    @app.route('/api/product/delete', methods=['GET'])
    def delete_product_api():
        id = request.args.get('id')
        if id is None:
            return Utilities.response("Missing parameters", status=400, success=False)
        try:
            ProductServices.delete_product(id)
        except Exception as e:
            return Utilities.response(str(e), status=400, success=False)
        return redirect('/dashboard')
