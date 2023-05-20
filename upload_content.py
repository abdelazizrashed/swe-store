import json
import os

from app.logic.modules.product.services import ProductServices
from app.logic.utilities import Utilities

file = open("content/products.json", "r")

products = json.load(file)

print(len(products["products"]))
for product in products["products"]:
    print("****************")
    print("uploading product: ", product["name"])
    name = product["name"]
    description = product["description"]
    price = product["price"]
    image_path = product["image_path"]
    category = product["category"]
    url = Utilities.upload_img(img_path=os.path.join(
        "content", image_path), db_path="products")

    res = ProductServices.create_product(
        name=name, description=description, img=url, price=price, category=category)
    print("product uploaded: ", res)
