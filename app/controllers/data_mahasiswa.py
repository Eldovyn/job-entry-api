from flask import jsonify
import cloudinary.api
from ..databases import UserDatabase, BatchDatabase


class DataMahasiswaController:
    @staticmethod
    async def get_data_mahasiswa_title_id(user_id, q, limit, per_page, current_page):
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
        data_mahasiswa = []
        if data_mahasiswa_title := await BatchDatabase.get(
            "title_data_mahasiswa", title=q, limit=limit
        ):
            data_mahasiswa.extend(data_mahasiswa_title)
        if data_mahasisw_id := await BatchDatabase.get("data_mahasiswa", user_id=q):
            data_mahasiswa.extend([data_mahasisw_id])
        if not data_mahasiswa:
            return jsonify({"message": "batch not found"}), 404
        per_page = int(per_page) if per_page else 10
        current_page = int(current_page) if current_page else 1

        paginated_data = [
            data_mahasiswa[i : i + per_page]
            for i in range(0, len(data_mahasiswa), per_page)
        ]
        paginated_data_mahasiswaes_dict = [
            [data_mahasiswa.to_dict() for data_mahasiswa in page]
            for page in paginated_data
        ]

        avatar_url = cloudinary.api.resource_by_asset_id(user.user_avatar.avatar)[
            "secure_url"
        ]
        total_pages = len(paginated_data_mahasiswaes_dict)
        current_page = (
            min(current_page, total_pages)
            if current_page <= total_pages
            else total_pages
        )
        paginated_items = (
            paginated_data_mahasiswaes_dict[current_page - 1]
            if current_page <= total_pages
            else paginated_data_mahasiswaes_dict[-1]
        )

        response_data = {
            "message": "success get all data_mahasiswa",
            "data": [item.to_dict() for item in data_mahasiswa],
            "page": {
                "current_page": current_page,
                "current_data": paginated_items,
                "total_pages": total_pages,
                "total_items": len(data_mahasiswa),
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
    async def get_all_data_mahasiswa(user_id, limit, per_page, current_page):
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

        batch = await BatchDatabase.get("all_data_mahasiswa", limit=limit)
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

        avatar_url = cloudinary.api.resource_by_asset_id(user.user_avatar.avatar)[
            "secure_url"
        ]
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
            "message": "success get all data mahasiswa",
            "data": [item.to_dict() for item in batch],
            "page": {
                "current_page": current_page,
                "current_data": paginated_items,
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
