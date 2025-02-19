from flask import jsonify, url_for
import datetime
from ..databases import AccountActiveDatabase, UserDatabase
from ..utils import TokenAccountActiveEmail, TokenAccountActiveWeb, generate_id
from ..task import send_email_task
from ..config import job_entry_url


class AccountActiveController:
    @staticmethod
    async def user_account_active_page(token):
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
        if not (valid_token := await TokenAccountActiveWeb.get(token)):
            return jsonify({"message": "token not found"}), 404
        if not (
            user_token := await AccountActiveDatabase.get(
                "account_active", user_id=valid_token["user_id"], token_web=token
            )
        ):
            return jsonify({"message": "token not found"}), 404
        if user_token.token_web != token:
            return jsonify({"message": "token not found"}), 404
        if user_token.expired_at <= int(created_at):
            await AccountActiveDatabase.delete(
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
    async def re_send_user_account_active(email):
        errors = {}
        if len(email.strip()) == 0:
            errors["email"] = ["email cannot be empty"]
        if errors:
            return (
                jsonify(
                    {
                        "message": "data is not valid",
                        "errors": errors,
                    }
                ),
                400,
            )
        if not (user := await UserDatabase.get("email", email=email)):
            return (
                jsonify({"message": "user not found"}),
                404,
            )
        if user.is_active:
            return (
                jsonify(
                    {
                        "message": "user already active",
                    }
                ),
                409,
            )
        if not (
            user_token := await AccountActiveDatabase.get(
                "user_id", user_id=user.user_id
            )
        ):
            return (
                jsonify({"message": "user not found"}),
                404,
            )
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if user_token.expired_at <= int(created_at):
            await AccountActiveDatabase.delete("user_id", user_id=user.user_id)
            return (
                jsonify({"message": "user not found"}),
                404,
            )
        expired_at = created_at + 300
        email_token = await TokenAccountActiveEmail.insert(
            f"{user.user_id}", int(created_at)
        )
        web_token = await TokenAccountActiveWeb.insert(
            f"{user.user_id}", int(created_at)
        )
        await AccountActiveDatabase.update(
            "token",
            token_email=email_token,
            token_web=web_token,
            expired_at=expired_at,
            updated_at=created_at,
            user_id=user_token.user_id,
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
                    "message": "success send email active account",
                    "data": {
                        "user_id": user.user_id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
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
            201,
        )

    @staticmethod
    async def user_account_active_verification(token):
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
        valid_token = await TokenAccountActiveEmail.get(token)
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
            user_token := await AccountActiveDatabase.get(
                "account_active_email",
                user_id=valid_token["user_id"],
                token_email=token,
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
            await AccountActiveDatabase.delete(
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
        await AccountActiveDatabase.update(
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
    async def user_account_active_verification_validation(token):
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
        valid_token = await TokenAccountActiveEmail.get(token)
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
            user_token := await AccountActiveDatabase.get(
                "account_active_email",
                user_id=valid_token["user_id"],
                token_email=token,
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
            await AccountActiveDatabase.delete(
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
