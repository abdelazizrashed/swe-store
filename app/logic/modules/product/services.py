from typing import List

from app.logic.firestore_db import db

from .model import ProductModel


class ProductServices:

    @staticmethod
    def create_product(name: str, description: str, img: str, price: float, category: str) -> ProductModel:
        update_time, product_ref = db.collection('products').add({
            'name': name,
            'description': description,
            'image': img,
            'price': price,
            'category': category
        })

        final_dict = product_ref.get().to_dict()
        final_dict['id'] = product_ref.id

        return ProductModel.from_dict(final_dict)

    @staticmethod
    def get_products() -> List[ProductModel]:
        products = db.collection('products').get()
        products_list: list[ProductModel] = []
        for product in products:
            product_dict = product.to_dict()
            product_dict['id'] = product.id
            products_list.append(ProductModel.from_dict(product_dict))
        return products_list

    @staticmethod
    def get_product(product_id: str) -> ProductModel:
        product = db.collection('products').document(product_id).get()
        product_dict = product.to_dict()
        product_dict['id'] = product.id
        product = ProductModel.from_dict(product_dict)
        return product

    @staticmethod
    def update_product(product_id: str = None, name: str = None, description: str = None, img: str = None, price: float = None) -> ProductModel:
        product = db.collection('products').document(product_id).get()
        product_dict = product.to_dict()
        if name is not None:
            product_dict['name'] = name
        if description is not None:
            product_dict['description'] = description
        if img is not None:
            product_dict['image'] = img
        if price is not None:
            product_dict['price'] = price
        db.collection('products').document(product_id).set(product_dict)
        product_dict['id'] = product.id
        return ProductModel.from_dict(product_dict)

    @staticmethod
    def delete_product(product_id: str) -> None:
        db.collection('products').document(product_id).delete()
