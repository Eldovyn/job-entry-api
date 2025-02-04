from ..databases import BatchDatabase, UserDatabase
from flask import jsonify
import datetime
from ..utils import generate_id


class BatchFormController:
    @staticmethod
    async def get_batch_id(user_id, batch_id):
        errors = {}
        if len(batch_id.strip()) == 0:
            errors["batch_id"] = ["batch id cannot be empty"]
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
        if not (batch := await BatchDatabase.get("batch_id", batch_id=batch_id)):
            return jsonify({"message": "batch not found"}), 404
        return (
            jsonify(
                {
                    "message": f"success get batch {batch_id!r}",
                    "data": {
                        "batch_id": batch.batch_form_id,
                        "title": batch.title,
                        "description": batch.description,
                        "created_at": batch.created_at,
                        "updated_at": batch.created_at,
                        "author": batch.user.username,
                        "is_active": batch.is_active,
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def get_all_batch(user_id):
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
        batch = await BatchDatabase.get("all_batch")
        return (
            jsonify(
                {
                    "message": "success add batch",
                    "data": [
                        {
                            "batch_id": item.batch_form_id,
                            "title": item.title,
                            "description": item.description,
                            "created_at": item.created_at,
                            "updated_at": item.created_at,
                            "author": item.user.username,
                            "is_active": item.is_active,
                        }
                        for item in batch
                    ],
                }
            ),
            200,
        )

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
