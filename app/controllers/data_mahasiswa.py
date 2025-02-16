from flask import jsonify
import cloudinary.api
from ..databases import UserDatabase, BatchDatabase


class DataMahasiswaController:
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
