from app.logic.firestore_db import db

from .models import UserModel


class AuthServices:

    @staticmethod
    def create_user(email: str, password: str, name: str) -> UserModel:
        users = db.collection('users').where('email', '==', email).get()
        if len(users) > 0:
            raise Exception('User already exists')
        _, user_ref = db.collection('users').add({
            'email': email,
            'password': password,
            'name': name,
        })

        user_dict = user_ref.get().to_dict()
        user_dict['id'] = user_ref.id
        return UserModel.from_dict(user_dict)

    @staticmethod
    def get_user(email: str) -> UserModel:
        users = db.collection(
            'users').where('email', '==', email).get()
        if len(users) == 0:
            raise Exception('User not found')
        user_ref = users[0]
        user_dict = user_ref.to_dict()
        user_dict['id'] = user_ref.id
        return UserModel.from_dict(user_dict)

    @staticmethod
    def login(email: str, password: str) -> UserModel:
        users = users = db.collection(
            'users').where('email', '==', email).get()
        if len(users) == 0:
            raise Exception('User not found')
        user_dict = users[0].to_dict()
        user_dict['id'] = users[0].id
        user = UserModel.from_dict(user_dict)
        if user.password != password:
            raise Exception('Password incorrect')
        return user
