from flask import jsonify
from ..databases import UserDatabase, AnnountcementDatabase
from ..utils import generate_id


class AnnountcementController:
    @staticmethod
    async def annountcement_post(user_id, title, content):
        errors = {}

        if len(title.strip()) == 0:
            errors["title"] = ["title cannot be empty"]
        if len(content.strip()) == 0:
            errors["content"] = ["content cannot be empty"]

        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization invalid"}),
                401,
            )
        if not user.is_admin:
            return (
                jsonify({"message": "authorization invalid"}),
                401,
            )

        annountcement_id = generate_id()
        data = await AnnountcementDatabase.insert(
            annountcement_id, user_id, title, content
        )
        return (
            jsonify({"message": "success post annountcement", "data": data.to_dict()}),
            201,
        )
