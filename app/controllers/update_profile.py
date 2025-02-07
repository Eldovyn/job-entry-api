from flask import jsonify
from ..utils import Validation
from ..databases import UserDatabase
import datetime
import cloudinary.api
import cloudinary.uploader
import os
from werkzeug.datastructures import FileStorage


class UpdateProfileController:
    @staticmethod
    async def update_user_avatar(user_id, avatar):
        errors = {}
        valid_image_extensions = [".jpg", ".jpeg", ".png"]
        MAX_FILE_SIZE = 500 * 1024
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()

        if not isinstance(avatar, FileStorage):
            errors["avatar"] = ["avatar must be a file"]
        else:
            _, ext = os.path.splitext(avatar.filename)

            if ext.lower() not in valid_image_extensions:
                errors["security_avatar"] = ["avatar only accept jpeg/png/jpg"]

            avatar_content = avatar.read()
            if len(avatar_content) > MAX_FILE_SIZE:
                errors.setdefault("security_avatar", []).append("avatar too large")

            if len(avatar_content) == 0:
                errors.setdefault("security_avatar", []).append("avatar file is empty")

            avatar.seek(0)

        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400

        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return jsonify({"message": "authorization invalid"}), 401

        result = cloudinary.uploader.upload(avatar, folder="avatars/")
        user_avatar = await UserDatabase.update(
            "avatar",
            user_id=user_id,
            new_avatar=result["asset_id"],
            created_at=created_at,
        )

        return (
            jsonify(
                {
                    "message": "success update avatar",
                    "data": {
                        "user_id": user_avatar.user.user_id,
                        "username": user_avatar.user.username,
                        "email": user_avatar.user.email,
                        "is_active": user_avatar.user.is_active,
                        "avatar": result["secure_url"],
                        "created_at": user_avatar.user.created_at,
                        "updated_at": user_avatar.user.updated_at,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def update_user_email(user_id, email, confirm_email):
        errors = {}
        if len(email.strip()) == 0:
            errors["email"] = ["email cannot be empty"]
        if len(confirm_email.strip()) == 0:
            errors["confirm_email"] = ["confirm email cannot be empty"]
        if not errors.get("email") and not errors.get("confirm_email"):
            if email != confirm_email:
                errors["security_email"] = ["email not match"]
            else:
                if not (email_valid := await Validation.validate_email(email)):
                    errors.setdefault("security_email", []).append("email not valid")
        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization invalid"}),
                401,
            )
        if user.email == email:
            return (
                jsonify({"message": "email cannot be the same"}),
                409,
            )
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        try:
            user_email = await UserDatabase.update(
                "email",
                user_id=user_id,
                new_email=email,
                created_at=created_at,
            )
        except Exception:
            return jsonify({"message": "email already exists"}), 409
        avatar_url = cloudinary.api.resource_by_asset_id(user.user_avatar.avatar)[
            "secure_url"
        ]
        return (
            jsonify(
                {
                    "message": "success update email",
                    "data": {
                        "user_id": user.user_id,
                        "username": user.username,
                        "email": user_email.email,
                        "is_active": user.is_active,
                        "avatar": avatar_url,
                        "created_at": user.created_at,
                        "updated_at": user.updated_at,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def update_user_username(user_id, username, confirm_username):
        errors = {}
        if len(username.strip()) == 0:
            errors["username"] = ["username cannot be empty"]
        if len(confirm_username.strip()) == 0:
            errors["confirm_username"] = ["confirm username cannot be empty"]
        if not errors.get("username") and not errors.get("confirm_username"):
            if username != confirm_username:
                errors["security_username"] = ["username not match"]
        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization invalid"}),
                401,
            )
        if user.username == username:
            return (
                jsonify({"message": "username cannot be the same"}),
                409,
            )
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        try:
            user_username = await UserDatabase.update(
                "username",
                user_id=user_id,
                new_username=username,
                created_at=created_at,
            )
        except Exception:
            return jsonify({"message": "username already exists"}), 409
        avatar_url = cloudinary.api.resource_by_asset_id(user.user_avatar.avatar)[
            "secure_url"
        ]
        return (
            jsonify(
                {
                    "message": "success update username",
                    "data": {
                        "user_id": user.user_id,
                        "username": user.username,
                        "username": user_username.username,
                        "is_active": user.is_active,
                        "is_admin": user.is_admin,
                        "avatar": avatar_url,
                        "created_at": user.created_at,
                        "updated_at": user.updated_at,
                    },
                }
            ),
            201,
        )
