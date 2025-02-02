from .database import Database
from ..models import UserModel, UserAvatarModel
from ..database import db


class UserDatabase(Database):
    @staticmethod
    async def insert(user_id, email, username, password, avatar_id, avatar, created_at):
        user = UserModel(
            email=email,
            username=username,
            password=password,
            user_id=user_id,
            created_at=created_at,
        )
        avatar = UserAvatarModel(user_id=user_id, avatar_id=avatar_id, avatar=avatar)
        db.session.add(user)
        db.session.add(avatar)
        db.session.commit()
        return user

    @staticmethod
    async def get(category, **kwargs):
        email = kwargs.get("email")
        user_id = kwargs.get("user_id")
        if category == "email":
            return UserModel.query.filter(UserModel.email == email).first()
        if category == "user_id":
            return UserModel.query.filter(UserModel.user_id == user_id).first()

    @staticmethod
    async def delete():
        pass

    @staticmethod
    async def update(category, **kwargs):
        user_id = kwargs.get("user_id")
        new_password = kwargs.get("new_password")
        created_at = kwargs.get("created_at")
        new_email = kwargs.get("new_email")
        new_username = kwargs.get("new_username")
        if category == "password":
            if user := UserModel.query.filter(UserModel.user_id == user_id).first():
                user.password = new_password
                user.updated_at = created_at
                db.session.commit()
                return user
        if category == "email":
            if user := UserModel.query.filter(UserModel.user_id == user_id).first():
                user.email = new_email
                user.updated_at = created_at
                db.session.commit()
                return user
        if category == "username":
            if user := UserModel.query.filter(UserModel.user_id == user_id).first():
                user.username = new_username
                user.updated_at = created_at
                db.session.commit()
                return user
