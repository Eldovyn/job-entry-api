from ..databases import ResetPasswordDatabase, UserDatabase
from flask import jsonify, url_for, request, render_template, redirect
import datetime
from ..utils import (
    TokenResetPasswordEmail,
    generate_id,
    TokenResetPasswordWeb,
    Validation,
)
from ..config import job_entry_url
import re
from ..task import send_email_task


class ResetPasswordController:
    @staticmethod
    async def get_page_user_reset_password(token):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if len(token.strip()) == 0:
            return (
                jsonify(
                    {
                        "message": "token cannot be empty",
                        "errors": {"token": ["token cannot be empty"]},
                    }
                ),
                400,
            )
        if not (valid_token := await TokenResetPasswordWeb.get(token)):
            return jsonify({"message": "token not found"}), 404
        if not (
            user_token := await ResetPasswordDatabase.get(
                "reset_password_web", user_id=valid_token["user_id"], web_token=token
            )
        ):
            return jsonify({"message": "token not found"}), 404
        if user_token.token_web != token:
            return jsonify({"message": "token not found"}), 404
        if user_token.expired_at <= int(created_at):
            await ResetPasswordDatabase.delete(
                "user_id", user_id=valid_token["user_id"]
            )
            return jsonify({"message": "token not found"}), 404
        return (
            jsonify(
                {
                    "message": "success get user token",
                    "data": {
                        "token": token,
                        "user_id": user_token.user.user_id,
                        "email": user_token.user.email,
                        "username": user_token.user.username,
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def re_send_user_reset_password(email):
        errors = {}
        if len(email.strip()) == 0:
            errors["email"] = ["email cannot be empty"]
        if not (email_valid := await Validation.validate_email(email)):
            if "email" in errors:
                errors["email"].append("email not valid")
            else:
                errors["email"] = ["email not valid"]
        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user := await UserDatabase.get("email", email=email)):
            return (
                jsonify({"message": "user not found"}),
                404,
            )
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if not (
            user_token := await ResetPasswordDatabase.get(
                "token_active", user_id=user.user_id
            )
        ):
            return (
                jsonify({"message": "user not found"}),
                404,
            )
        if user_token.expired_at <= int(created_at):
            await ResetPasswordDatabase.delete("user_id", user_id=user.user_id)
            return (
                jsonify({"message": "user not found"}),
                404,
            )
        expired_at = created_at + 300
        token_email = await TokenResetPasswordEmail.insert(
            f"{user.user_id}", int(created_at)
        )
        token_web = await TokenResetPasswordWeb.insert(
            f"{user.user_id}", int(created_at)
        )
        await ResetPasswordDatabase.update(
            "token_active",
            user_id=user.user_id,
            token_email=token_email,
            token_web=token_web,
            expired_at=int(expired_at),
            updated_at=int(created_at),
        )
        send_email_task.apply_async(
            args=[
                "Reset Password",
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
    <p>Someone has requested a link to change your password, and you can do this through the link below.</p>
    <p>
        <a href="{job_entry_url}/reset-password?token={token_email}">
            Click here to reset your password
        </a>
    </p>
    <p>If you didn't request this, please ignore this email.</p>
    <p>Your password won't change until you access the link above and create a new one.</p>
</body>
</html>
""",
                "reset password",
            ],
        )
        return (
            jsonify(
                {
                    "message": "success send reset password",
                    "data": {
                        "user_id": user.user_id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                    },
                    "reset_password": {
                        "token": user_token.token_web,
                        "created_at": user_token.created_at,
                        "updated_at": user_token.updated_at,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def get_user_reset_password(token):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if len(token.strip()) == 0:
            return (
                jsonify(
                    {
                        "message": "token cannot be empty",
                        "errors": {"token": ["token cannot be empty"]},
                    }
                ),
                400,
            )
        valid_token = await TokenResetPasswordEmail.get(token)
        if not valid_token:
            return (
                jsonify(
                    {
                        "message": "token not found",
                    }
                ),
                404,
            )
        if not (
            user_token := await ResetPasswordDatabase.get(
                "reset_password_email",
                user_id=valid_token["user_id"],
                email_token=token,
            )
        ):
            return (
                jsonify(
                    {
                        "message": "token not found",
                    }
                ),
                404,
            )
        if user_token.expired_at <= int(created_at):
            await ResetPasswordDatabase.delete(
                "user_id", user_id=valid_token["user_id"]
            )
            return (
                jsonify(
                    {
                        "message": "token not found",
                    }
                ),
                404,
            )
        await ResetPasswordDatabase.update(
            "user_active", user_id=valid_token["user_id"], updated_at=created_at
        )
        return (
            jsonify(
                {
                    "message": "success get user token",
                    "data": {
                        "token": token,
                        "user_id": user_token.user.user_id,
                        "email": user_token.user.email,
                        "username": user_token.user.username,
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def user_reset_password(email):
        errors = {}
        if len(email.strip()) == 0:
            errors["email"] = ["email cannot be empty"]
        if not (email_valid := await Validation.validate_email(email)):
            if "email" in errors:
                errors["email"].append("email not valid")
            else:
                errors["email"] = ["email not valid"]
        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user := await UserDatabase.get("email", email=email)):
            return (
                jsonify({"message": "user not found"}),
                404,
            )
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        expired_at = created_at + 300
        token_email = await TokenResetPasswordEmail.insert(
            f"{user.user_id}", int(created_at)
        )
        token_web = await TokenResetPasswordWeb.insert(
            f"{user.user_id}", int(created_at)
        )
        if not (
            user_token := await ResetPasswordDatabase.insert(
                generate_id(),
                user.user_id,
                token_email,
                token_web,
                int(expired_at),
                int(created_at),
            )
        ):
            return (
                jsonify({"message": "user not found"}),
                404,
            )
        send_email_task.apply_async(
            args=[
                "Reset Password Netpoll",
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
    <p>Someone has requested a link to change your password, and you can do this through the link below.</p>
    <p>
        <a href="{job_entry_url}/reset-password?token={token_email}">
            Click here to reset your password
        </a>
    </p>
    <p>If you didn't request this, please ignore this email.</p>
    <p>Your password won't change until you access the link above and create a new one.</p>
</body>
</html>
""",
                "reset password",
            ],
        )
        return (
            jsonify(
                {
                    "message": "success send reset password",
                    "data": {
                        "user_id": user.user_id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                    },
                    "reset_password": {
                        "token": user_token.token_web,
                        "created_at": user_token.created_at,
                        "updated_at": user_token.updated_at,
                    },
                }
            ),
            201,
        )
