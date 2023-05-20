

class CartModel:
    user_id: str
    total_price: float
    number_of_products: int

    def __init__(self, user_id: str, total_price: float, number_of_products: int):
        self.user_id = user_id
        self.total_price = total_price
        self.number_of_products = number_of_products

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "total_price": self.total_price,
            "number_of_products": self.number_of_products
        }

    @staticmethod
    def from_dict(data: dict):
        return CartModel(
            user_id=data["user_id"],
            total_price=data["total_price"],
            number_of_products=data["number_of_products"]
        )

    def copyt_with(self, **kwargs):
        return CartModel(
            user_id=kwargs.get("user_id", self.user_id),
            total_price=kwargs.get("total_price", self.total_price),
            number_of_products=kwargs.get(
                "number_of_products", self.number_of_products)
        )


class CartProductModel:
    id: str
    user_id: str
    amount: int
    name: str
    price: float
    image: str

    def __init__(self, id: str, user_id: str, amount: int, name: str, price: float, image: str):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.name = name
        self.price = price
        self.image = image

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "name": self.name,
            "price": self.price,
            "image": self.image
        }

    @staticmethod
    def from_dict(data: dict):
        return CartProductModel(
            id=data["id"],
            user_id=data["user_id"],
            amount=data["amount"],
            name=data["name"],
            price=data["price"],
            image=data["image"]
        )

    def copyt_with(self, **kwargs):
        return CartProductModel(
            id=kwargs.get("id", self.id),
            user_id=kwargs.get("user_id", self.user_id),
            amount=kwargs.get("amount", self.amount),
            name=kwargs.get("name", self.name),
            price=kwargs.get("price", self.price),
            image=kwargs.get("image", self.image)
        )
