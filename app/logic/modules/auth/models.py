class UserModel:
    id: str
    email: str
    password: str
    name: str

    def __init__(self, id: str, email: str, password: str, name: str):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
        }

    @staticmethod
    def from_dict(data: dict):
        return UserModel(
            id=data['id'],
            email=data['email'],
            password=data['password'],
            name=data['name'],
        )

    def copy_with(self, **kwargs):
        return UserModel(
            id=kwargs.get('id', self.id),
            email=kwargs.get('email', self.email),
            password=kwargs.get('password', self.password),
            name=kwargs.get('name', self.name),
        )
