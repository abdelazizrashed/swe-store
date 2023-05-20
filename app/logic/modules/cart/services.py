from typing import List, Tuple

from app.logic.firestore_db import db
from app.logic.modules.cart.models import CartModel, CartProductModel

from ..product.services import ProductServices


class CartServices:

    @staticmethod
    def add_to_cart(user_id: str, product_id: str, amount: int) -> Tuple[CartModel, List[CartProductModel]]:

        product = ProductServices.get_product(product_id)
        cart_product = CartServices.get_cart_product(user_id, product_id)
        if cart_product is None:
            db.collection("cart").document(user_id).collection("products").document(product_id).set({
                "id": product_id,
                "user_id": user_id,
                "amount": amount,
                "name": product.name,
                "price": product.price,
                "image": product.image
            })
        else:
            cart_product.amount += amount
            db.collection("cart").document(user_id).collection("products").document(product_id).update(
                {"amount": cart_product.amount})
        products = CartServices.get_cart_products(user_id)
        total_price = sum(
            [product.price * product.amount for product in products])
        cart_dict = {
            "user_id": user_id,
            "total_price": total_price,
            'number_of_products': len(products),
        }
        db.collection("cart").document(user_id).set(cart_dict)
        return CartModel.from_dict(cart_dict), products

    @staticmethod
    def remove_product(user_id: str, product_id: str) -> Tuple[CartModel, List[CartProductModel]]:
        db.collection("cart").document(user_id).collection(
            "products").document(product_id).delete()
        products = CartServices.get_cart_products(user_id)
        total_price = sum(
            [product.price * product.amount for product in products])
        cart_dict = {
            "user_id": user_id,
            "total_price": total_price,
            'number_of_products': len(products),
        }
        db.collection("cart").document(user_id).set(cart_dict)
        return CartModel.from_dict(cart_dict), products

    @staticmethod
    def empty_cart(user_id: str) -> None:
        docs = db.collection("cart").document(user_id).collection(
            "products").list_documents()
        for doc in docs:
            doc.delete()
        db.collection("cart").document(user_id).delete()

    @staticmethod
    def remove_amount(user_id: str, product_id: str, amount: int) -> Tuple[CartModel, List[CartProductModel]]:
        cart_product = CartServices.get_cart_product(user_id, product_id)
        if cart_product is None:
            raise Exception("Product not found in cart")
        if cart_product.amount <= amount:
            CartServices.remove_product(user_id, product_id)
        else:
            new_amount = cart_product.amount - amount
            db.collection("cart").document(user_id).collection("products").document(product_id).update(
                {"amount": new_amount})
        products = CartServices.get_cart_products(user_id)
        total_price = sum(
            [product.price * product.amount for product in products])
        cart_dict = {
            "user_id": user_id,
            "total_price": total_price,
            'number_of_products': len(products),
        }
        db.collection("cart").document(user_id).set(cart_dict)
        return CartModel.from_dict(cart_dict), products

    @staticmethod
    def get_cart_product(user_id: str, product_id: str) -> CartProductModel:
        cart_product = db.collection("cart").document(user_id).collection(
            "products").document(product_id).get().to_dict()
        if cart_product is None:
            return None
        return CartProductModel.from_dict(cart_product)

    @staticmethod
    def get_cart_products(user_id: str) -> List[CartProductModel]:
        cart_products = db.collection("cart").document(
            user_id).collection("products").get()
        return [CartProductModel.from_dict(cart_product.to_dict()) for cart_product in cart_products]

    @staticmethod
    def get_cart(user_id: str) -> CartModel:
        cart = db.collection("cart").document(user_id).get().to_dict()
        if cart is None:
            return None
        return CartModel.from_dict(cart)
