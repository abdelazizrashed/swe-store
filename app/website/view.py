import json
import os

import jinja2
from flask import Blueprint, Flask, redirect, render_template, request, session

from ..logic.modules.cart.services import CartServices
from ..logic.modules.product.services import ProductServices


def create_app():

    app = Blueprint('website', __name__,
                    template_folder='templates', static_folder='static')

    @app.route('/')
    def shop():
        products = ProductServices.get_products()

        user_id = session.get('user_id')
        if user_id is None:
            number_of_products = 0
        else:
            cart = CartServices.get_cart(user_id)
            if cart is None:
                number_of_products = 0
            else:
                number_of_products = cart.number_of_products
        return render_template(
            'shop.html',
            products=[p.to_dict() for p in products],
            cart=number_of_products,
        )

    @app.route('/product')
    def product():
        product = ProductServices.get_product(request.args.get('id'))
        products = ProductServices.get_products()[0:5]
        user_id = session.get('user_id')
        if user_id is None:
            number_of_products = 0
        else:
            cart = CartServices.get_cart(user_id)
            if cart is None:
                number_of_products = 0
            else:
                number_of_products = cart.number_of_products

        return render_template(
            'shop-single.html',
            product=product.to_dict(),
            products=[p.to_dict() for p in products],
            cart=number_of_products,
        )

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    @ app.route('/cart')
    def cart():

        user_id = session.get('user_id')
        if user_id is None:
            Exception('User not logged in')
        cart = CartServices.get_cart(user_id)
        if cart is None:
            return redirect('/')
        else:
            number_of_products = cart.number_of_products
        cart_products = CartServices.get_cart_products(user_id)
        return render_template(
            'cart.html',
            cart=number_of_products,
            cart_data=cart.to_dict(),
            products=[p.to_dict()
                      for p in cart_products],
            products_json=[json.dumps(p.to_dict()) for p in cart_products],
        )

    @app.route('/thankyou')
    def thankyou():
        CartServices.empty_cart(session.get('user_id'))
        return render_template('thankyou.html', cart=0)

    @app.route('/dashboard')
    def admin():

        user_id = session.get('user_id')
        if user_id is None:
            return redirect('/login')
        products = ProductServices.get_products()
        return render_template(
            'products.html',
            products=[product.to_dict() for product in products]
        )

    @app.route('/dashboard/users')
    def users():

        user_id = session.get('user_id')
        if user_id is None:
            return redirect('/login')
        return render_template('users.html')

    @app.route('/dashboard/product')
    def admin_product():

        user_id = session.get('user_id')
        if user_id is None:
            return redirect('/login')
        id = request.args.get('id')
        if id is not None:
            product = ProductServices.get_product(id)
            return render_template('product.html', product=product.to_dict())
        return render_template('product.html', product=None)

    return app
