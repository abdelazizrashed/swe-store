class ProductModel:
    id: str
    name: str
    description: str
    price: float
    image: str
    category: str

    def __init__(self, name: str, description: str, price: float, image: str, category: str, id: str = None):
        self.name = name
        self.description = description
        self.price = price
        self.image = image
        self.id = id
        self.category = category

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image': self.image,
            'id': self.id,
            'category': self.category
        }

    @staticmethod
    def from_dict(data: dict):
        return ProductModel(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            price=data['price'],
            image=data['image'],
            category=data['category']
        )

    def __str__(self) -> str:
        return f'ProductModel(id={self.id}, name={self.name}, description={self.description}, price={self.price}, image={self.image}, category={self.category})'
