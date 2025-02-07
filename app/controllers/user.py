from ..databases import UserDatabase, TokenBlacklistDatabase, AccountActiveDatabase
from flask import jsonify
import sqlalchemy
from flask_jwt_extended import create_access_token
import re
import datetime
from ..utils import (
    TokenAccountActiveEmail,
    TokenAccountActiveWeb,
    generate_id,
    Validation,
)
from ..task import send_email_task
from ..config import job_entry_url
import cloudinary.api


class UserController:
    @staticmethod
    async def user_me(user_id):
        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization invalid"}),
                401,
            )
        avatar_url = cloudinary.api.resource_by_asset_id(user.user_avatar.avatar)[
            "secure_url"
        ]
        return (
            jsonify(
                {
                    "message": "success get user",
                    "data": {
                        "user_id": user.user_id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                        "is_admin": user.is_admin,
                        "avatar": avatar_url,
                        "created_at": user.created_at,
                        "updated_at": user.updated_at,
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def user_logout(jti):
        await TokenBlacklistDatabase.insert(
            generate_id(), jti, datetime.datetime.now(datetime.timezone.utc).timestamp()
        )
        return jsonify({"message": "success logout"}), 201

    @staticmethod
    async def user_login(email, password):
        from ..bcrypt import bcrypt

        errors = {}
        if len(email.strip()) == 0:
            errors["email"] = ["email cannot be empty"]
        if len(password.strip()) == 0:
            errors["password"] = ["password cannot be empty"]
        if not (email_valid := await Validation.validate_email(email)):
            if "email" in errors:
                errors["email"].append("email not valid")
            else:
                errors["email"] = ["email not valid"]
        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user := await UserDatabase.get("email", email=email)):
            return jsonify({"message": "failed login"}), 404
        if not bcrypt.check_password_hash(user.password, password):
            return (
                jsonify({"message": "authorization invalid", "data": {"email": email}}),
                401,
            )
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        avatar_url = cloudinary.api.resource_by_asset_id(user.user_avatar.avatar)[
            "secure_url"
        ]
        if not user.is_active:
            expired_at = created_at + 300
            email_token = await TokenAccountActiveEmail.insert(
                f"{user.user_id}", int(created_at)
            )
            web_token = await TokenAccountActiveWeb.insert(
                f"{user.user_id}", int(created_at)
            )
            user_token = await AccountActiveDatabase.insert(
                generate_id(),
                f"{user.user_id}",
                email_token,
                web_token,
                int(expired_at),
                created_at,
            )
            send_email_task.apply_async(
                args=[
                    "Account Active",
                    [user.email],
                    f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>
<body>
    <p>Hello {user.username},</p>
    <p>Someone has requested a link to verify your account, and you can do this through the link below.</p>
    <p>
        <a href="{job_entry_url}/account-active?token={email_token}">
            Click here to activate your account
        </a>
    </p>
    <p>If you didn't request this, please ignore this email.</p>
</body>
</html>
                    """,
                    "account active",
                ],
            )
            return (
                jsonify(
                    {
                        "message": "user inactive",
                        "data": {
                            "user_id": user.user_id,
                            "username": user.username,
                            "email": user.email,
                            "is_active": user.is_active,
                            "is_admin": user.is_admin,
                            "avatar": avatar_url,
                            "created_at": user.created_at,
                            "updated_at": user.updated_at,
                        },
                        "account_active": {
                            "token": user_token.token_web,
                            "created_at": user_token.created_at,
                            "updated_at": user_token.updated_at,
                        },
                    }
                ),
                403,
            )
        access_token = create_access_token(identity=user)
        return (
            jsonify(
                {
                    "message": "success login",
                    "data": {
                        "user_id": user.user_id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                        "is_admin": user.is_admin,
                        "avatar": avatar_url,
                        "created_at": user.created_at,
                        "updated_at": user.updated_at,
                        "access_token": access_token,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def user_register(email, username, password, confirm_password, avatar):
        from ..bcrypt import bcrypt

        errors = {}
        if len(email.strip()) == 0:
            if "email" in errors:
                errors["email"].append("email cant be empety")
            else:
                errors["email"] = ["email cant be empety"]
        if len(username.strip()) == 0:
            if "username" in errors:
                errors["username"].append("username cant be empety")
            else:
                errors["username"] = ["username cant be empety"]
        if len(password.strip()) == 0:
            if "password" in errors:
                errors["password"].append("password cant be empety")
            else:
                errors["password"] = ["password cant be empety"]
        if len(email.strip()) > 0 and not (
            email_valid := await Validation.validate_email(email)
        ):
            if "email" in errors:
                errors["email"].append("email not valid")
            else:
                errors["email"] = ["email not valid"]
        if len(password.strip()) == 0:
            errors["password"] = ["password cannot be empty"]
        if len(confirm_password.strip()) == 0:
            errors["confirm_password"] = ["confirm password cannot be empty"]

        if not errors.get("password") and not errors.get("confirm_password"):
            if password != confirm_password:
                errors["security_password"] = ["password not match"]
            else:
                if len(password) < 8:
                    errors.setdefault("security_password", []).append(
                        "minimum 8 characters"
                    )
                if not re.search("[a-z]", password):
                    errors.setdefault("security_password", []).append(
                        "password must contain lowercase"
                    )
                if not re.search("[A-Z]", password):
                    errors.setdefault("security_password", []).append(
                        "password must contain uppercase"
                    )
                if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                    errors.setdefault("security_password", []).append(
                        "password must contain special character(s)"
                    )
                if not re.search(r"\d", password):
                    errors.setdefault("security_password", []).append(
                        "password must contain number"
                    )
        if errors:
            return (
                jsonify(
                    {
                        "message": "input invalid",
                        "errors": errors,
                    }
                ),
                400,
            )
        result_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user_id = generate_id()
        avatar_id = generate_id()
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        try:
            user = await UserDatabase.insert(
                user_id, email, username, result_password, avatar_id, avatar, created_at
            )
        except sqlalchemy.exc.IntegrityError:
            return (
                jsonify(
                    {
                        "message": "username or email already exists",
                        "data": {"username": username, "email": email},
                    },
                ),
                409,
            )
        expired_at = created_at + 300
        email_token = await TokenAccountActiveEmail.insert(
            f"{user.user_id}", int(created_at)
        )
        web_token = await TokenAccountActiveWeb.insert(
            f"{user.user_id}", int(created_at)
        )
        user_token = await AccountActiveDatabase.insert(
            generate_id(),
            f"{user.user_id}",
            email_token,
            web_token,
            int(expired_at),
            created_at,
        )
        send_email_task.apply_async(
            args=[
                "Account Active",
                [user.email],
                f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>
<body>
    <p>Hello {user.username},</p>
    <p>Someone has requested a link to verify your account, and you can do this through the link below.</p>
    <p>
        <a href="{job_entry_url}/account-active?token={email_token}">
            Click here to activate your account
        </a>
    </p>
    <p>If you didn't request this, please ignore this email.</p>
</body>
</html>
                """,
                "account active",
            ],
        )
        return (
            jsonify(
                {
                    "message": "success register",
                    "data": {
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                        "updated_at": user.updated_at,
                        "user_id": user.user_id,
                        "created_at": user.created_at,
                    },
                    "account_active": {
                        "token": user_token.token_web,
                        "created_at": user_token.created_at,
                        "updated_at": user_token.updated_at,
                    },
                }
            ),
            201,
        )
