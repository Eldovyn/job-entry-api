from ..databases import BatchDatabase, UserDatabase
from flask import jsonify
import datetime
from ..utils import generate_id
import cloudinary


class BatchFormController:
    @staticmethod
    async def update_status_batch(user_id, batch_id, limit, per_page, current_page):
        errors = {}

        def validate_input(value, param_name):
            if value and not value.isdigit():
                return f"{param_name} must be a number"
            if value and value.isdigit():
                value = int(value)
                if value <= 0:
                    return f"{param_name} must be greater than 0"
            return value

        errors = {}

        limit = validate_input(limit, "limit")
        per_page = validate_input(per_page, "per_page")
        current_page = validate_input(current_page, "current_page")

        if isinstance(limit, str):
            errors["limit"] = [limit]
        if isinstance(per_page, str):
            errors["per_page"] = [per_page]
        if isinstance(current_page, str):
            errors["current_page"] = [current_page]

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
        if not (
            batch_data := await BatchDatabase.update(
                "status_batch_id", batch_id=batch_id, created_at=created_at
            )
        ):
            return jsonify({"message": "batch not found"}), 404
        if limit:
            batch = await BatchDatabase.get("all_batch", limit=limit)
        else:
            batch = await BatchDatabase.get("all_batch")
        paginated_data = [
            batch[i : i + per_page] for i in range(0, len(batch), per_page)
        ]
        paginated_batches_dict = [
            [batch.to_dict() for batch in page] for page in paginated_data
        ]
        avatar_url = cloudinary.CloudinaryImage(user.user_avatar.avatar).url
        return (
            jsonify(
                {
                    "message": f"success delete batch",
                    "data": batch_data.to_dict(),
                    "page": {
                        "total_page": len(paginated_batches_dict),
                        "batches": paginated_batches_dict,
                        "size": len(batch),
                        "current_page": current_page,
                        "limit": limit,
                        "per_page": per_page,
                    },
                    "user": {
                        "user_id": user.user_id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                        "is_admin": user.is_admin,
                        "avatar": avatar_url,
                        "created_at": user.created_at,
                        "updated_at": user.updated_at,
                    },
                },
            ),
            201,
        )

    @staticmethod
    async def delete_batch(user_id, batch_id, limit, per_page, current_page):
        errors = {}

        def validate_input(value, param_name):
            if value and not value.isdigit():
                return f"{param_name} must be a number"
            if value and value.isdigit():
                value = int(value)
                if value <= 0:
                    return f"{param_name} must be greater than 0"
            return value

        errors = {}

        limit = validate_input(limit, "limit")
        per_page = validate_input(per_page, "per_page")
        current_page = validate_input(current_page, "current_page")

        if isinstance(limit, str):
            errors["limit"] = [limit]
        if isinstance(per_page, str):
            errors["per_page"] = [per_page]
        if isinstance(current_page, str):
            errors["current_page"] = [current_page]

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
        if not (
            batch_data := await BatchDatabase.delete("batch_id", batch_id=batch_id)
        ):
            return jsonify({"message": "batch not found"}), 404
        if limit:
            batch = await BatchDatabase.get("all_batch", limit=limit)
        else:
            batch = await BatchDatabase.get("all_batch")

        per_page = int(per_page) if per_page else 10
        current_page = int(current_page) if current_page else 1

        paginated_data = [
            batch[i : i + per_page] for i in range(0, len(batch), per_page)
        ]
        paginated_batches_dict = [
            [batch.to_dict() for batch in page] for page in paginated_data
        ]

        avatar_url = cloudinary.CloudinaryImage(user.user_avatar.avatar).url
        total_pages = len(paginated_batches_dict)
        current_page = (
            min(current_page, total_pages)
            if current_page <= total_pages
            else total_pages
        )
        paginated_items = (
            paginated_batches_dict[current_page - 1]
            if current_page <= total_pages
            else paginated_batches_dict[-1]
        )

        response_data = {
            "message": "success delete batch",
            "data": batch_data.to_dict(),
            "page": {
                "current_page": current_page,
                "current_batch": paginated_items,
                "total_pages": total_pages,
                "total_items": len(batch),
                "items_per_page": per_page,
                "limit": limit,
                "next_page": current_page + 1 if current_page < total_pages else None,
                "previous_page": current_page - 1 if current_page > 1 else None,
            },
            "user": {
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

        return jsonify(response_data), 201

    @staticmethod
    async def get_batch_title_id(role, user_id, q, limit, per_page, current_page):
        errors = {}
        if len(q.strip()) == 0:
            errors["q"] = ["query cannot be empty"]
        if limit and not limit.isdigit():
            errors["limit"] = ["limit must be a number"]
        if limit and limit.isdigit():
            limit = int(limit)
            if limit <= 0:
                errors.setdefault("limit", []).append("limit must be greater than 0")
        if per_page and not per_page.isdigit():
            errors["per_page"] = ["per_page must be a number"]
        if per_page and per_page.isdigit():
            per_page = int(per_page)
            if per_page <= 0:
                errors.setdefault("per_page", []).append(
                    "per_page must be greater than 0"
                )
        if current_page and not current_page.isdigit():
            errors["current_page"] = ["current_page must be a number"]
        if current_page and current_page.isdigit():
            current_page = int(current_page)
            if current_page < 0:
                errors.setdefault("current_page", []).append(
                    "current_page must be greater than 0"
                )
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
        batch = []
        if limit:
            if batch_title := await BatchDatabase.get(
                "title", title=q, limit=limit, role=role
            ):
                batch.extend(batch_title)
        else:
            if batch_title := await BatchDatabase.get("title", title=q, role=role):
                batch.extend(batch_title)
        if batch_id := await BatchDatabase.get("batch_id", batch_id=q):
            batch.extend([batch_id])
        if not batch:
            return jsonify({"message": "batch not found"}), 404
        per_page = int(per_page) if per_page else 10
        current_page = int(current_page) if current_page else 1

        paginated_data = [
            batch[i : i + per_page] for i in range(0, len(batch), per_page)
        ]
        paginated_batches_dict = [
            [batch.to_dict() for batch in page] for page in paginated_data
        ]

        avatar_url = cloudinary.CloudinaryImage(user.user_avatar.avatar).url
        total_pages = len(paginated_batches_dict)
        current_page = (
            min(current_page, total_pages)
            if current_page <= total_pages
            else total_pages
        )
        paginated_items = (
            paginated_batches_dict[current_page - 1]
            if current_page <= total_pages
            else paginated_batches_dict[-1]
        )

        response_data = {
            "message": "success get all batch",
            "data": [item.to_dict() for item in batch],
            "page": {
                "current_page": current_page,
                "current_batch": paginated_items,
                "total_pages": total_pages,
                "total_items": len(batch),
                "items_per_page": per_page,
                "limit": limit,
                "next_page": current_page + 1 if current_page < total_pages else None,
                "previous_page": current_page - 1 if current_page > 1 else None,
            },
            "user": {
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

        return jsonify(response_data), 200

    @staticmethod
    async def get_all_batch(role, user_id, limit, per_page, current_page):
        def validate_input(value, param_name):
            if value and not value.isdigit():
                return f"{param_name} must be a number"
            if value and value.isdigit():
                value = int(value)
                if value <= 0:
                    return f"{param_name} must be greater than 0"
            return value

        errors = {}

        limit = validate_input(limit, "limit")
        per_page = validate_input(per_page, "per_page")
        current_page = validate_input(current_page, "current_page")

        if isinstance(limit, str):
            errors["limit"] = [limit]
        if isinstance(per_page, str):
            errors["per_page"] = [per_page]
        if isinstance(current_page, str):
            errors["current_page"] = [current_page]

        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400

        user = await UserDatabase.get("user_id", user_id=user_id)
        if not user or not user.is_admin:
            return jsonify({"message": "authorization invalid"}), 401

        batch = (
            await BatchDatabase.get("all_batch", limit=limit, role=role)
            if limit
            else await BatchDatabase.get("all_batch", role=role)
        )
        if not batch:
            return jsonify({"message": "batch not found"}), 404

        per_page = int(per_page) if per_page else 10
        current_page = int(current_page) if current_page else 1

        paginated_data = [
            batch[i : i + per_page] for i in range(0, len(batch), per_page)
        ]
        paginated_batches_dict = [
            [batch.to_dict() for batch in page] for page in paginated_data
        ]

        avatar_url = cloudinary.CloudinaryImage(user.user_avatar.avatar).url
        total_pages = len(paginated_batches_dict)
        current_page = (
            min(current_page, total_pages)
            if current_page <= total_pages
            else total_pages
        )
        paginated_items = (
            paginated_batches_dict[current_page - 1]
            if current_page <= total_pages
            else paginated_batches_dict[-1]
        )

        response_data = {
            "message": "success get all batch",
            "data": [item.to_dict() for item in batch],
            "page": {
                "current_page": current_page,
                "current_batch": paginated_items,
                "total_pages": total_pages,
                "total_items": len(batch),
                "items_per_page": per_page,
                "limit": limit,
                "next_page": current_page + 1 if current_page < total_pages else None,
                "previous_page": current_page - 1 if current_page > 1 else None,
            },
            "user": {
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

        return jsonify(response_data), 200

    @staticmethod
    async def add_batch(user_id, title, description, limit, per_page, current_page):
        errors = {}
        if len(description.strip()) == 0:
            errors["description"] = ["description cannot be empty"]
        if len(title.strip()) == 0:
            errors["title"] = ["title cannot be empty"]

        def validate_input(value, param_name):
            if value and not value.isdigit():
                return f"{param_name} must be a number"
            if value and value.isdigit():
                value = int(value)
                if value <= 0:
                    return f"{param_name} must be greater than 0"
            return value

        limit = validate_input(limit, "limit")
        per_page = validate_input(per_page, "per_page")
        current_page = validate_input(current_page, "current_page")

        if isinstance(limit, str):
            errors["limit"] = [limit]
        if isinstance(per_page, str):
            errors["per_page"] = [per_page]
        if isinstance(current_page, str):
            errors["current_page"] = [current_page]

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
        batch_data = await BatchDatabase.insert(
            user_id=user_id,
            batch_form_id=batch_id,
            title=title,
            description=description,
            created_at=created_at,
        )

        if limit:
            batch = await BatchDatabase.get("all_batch", limit=limit)
        else:
            batch = await BatchDatabase.get("all_batch")

        per_page = int(per_page) if per_page else 10
        current_page = int(current_page) if current_page else 1

        paginated_data = [
            batch[i : i + per_page] for i in range(0, len(batch), per_page)
        ]
        paginated_batches_dict = [
            [batch.to_dict() for batch in page] for page in paginated_data
        ]

        avatar_url = cloudinary.CloudinaryImage(user.user_avatar.avatar).url
        total_pages = len(paginated_batches_dict)
        current_page = (
            min(current_page, total_pages)
            if current_page <= total_pages
            else total_pages
        )
        paginated_items = (
            paginated_batches_dict[current_page - 1]
            if current_page <= total_pages
            else paginated_batches_dict[-1]
        )

        response_data = {
            "message": "success delete batch",
            "data": batch_data.to_dict(),
            "page": {
                "current_page": current_page,
                "current_batch": paginated_items,
                "total_pages": total_pages,
                "total_items": len(batch),
                "items_per_page": per_page,
                "limit": limit,
                "next_page": current_page + 1 if current_page < total_pages else None,
                "previous_page": current_page - 1 if current_page > 1 else None,
            },
            "user": {
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

        return jsonify(response_data), 201
