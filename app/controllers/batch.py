from ..databases import BatchDatabase, UserDatabase
from flask import jsonify
import datetime
from ..utils import generate_id


class BatchFormController:
    @staticmethod
    async def add_batch(user_id, title, description):
        errors = {}
        if len(description.strip()) == 0:
            errors["description"] = ["description cannot be empty"]
        if len(title.strip()) == 0:
            errors["title"] = ["title cannot be empty"]
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
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        batch_id = generate_id()
        batch = await BatchDatabase.insert(
            user_id=user_id,
            batch_form_id=batch_id,
            title=title,
            description=description,
            created_at=created_at,
        )
        return (
            jsonify(
                {
                    "message": "success add batch",
                    "data": {
                        "batch_id": batch_id,
                        "title": title,
                        "description": description,
                        "created_at": created_at,
                        "updated_at": created_at,
                        "author": user.username,
                        "is_active": batch.is_active,
                    },
                }
            ),
            200,
        )
