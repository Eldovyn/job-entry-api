from .database import Database
from ..models import UsersModel, UserAvatarModel
from ..database import db


class UserDatabase(Database):
    @staticmethod
    async def insert(user_id, email, username, password, avatar_id, avatar, created_at):
        user = UsersModel(
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
            return UsersModel.query.filter(UsersModel.email == email).first()
        if category == "user_id":
            return UsersModel.query.filter(UsersModel.user_id == user_id).first()

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
        new_avatar = kwargs.get("new_avatar")
        if category == "password":
            if user := UsersModel.query.filter(UsersModel.user_id == user_id).first():
                user.password = new_password
                user.updated_at = created_at
                db.session.commit()
                return user
        if category == "email":
            if user := UsersModel.query.filter(UsersModel.user_id == user_id).first():
                user.email = new_email
                user.updated_at = created_at
                db.session.commit()
                return user
        if category == "username":
            if user := UsersModel.query.filter(UsersModel.user_id == user_id).first():
                user.username = new_username
                user.updated_at = created_at
                db.session.commit()
                return user
        if category == "avatar":
            if user := UsersModel.query.filter(UsersModel.user_id == user_id).first():
                if user_avatar := UserAvatarModel.query.filter(
                    UserAvatarModel.user_id == user_id
                ).first():
                    user_avatar.user.updated_at = created_at
                    user_avatar.updated_at = created_at
                    user_avatar.avatar = new_avatar
                    db.session.commit()
                    return user_avatar
