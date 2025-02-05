from flask import Blueprint, request
from ..controllers import BatchFormController
from flask_jwt_extended import jwt_required, get_jwt_identity

batch_form_router = Blueprint("batch_form_router", __name__)
batch_form_controller = BatchFormController()


@batch_form_router.post("/job-entry/admin/batch")
@jwt_required()
async def add_batch():
    current_user = get_jwt_identity()
    data = request.json
    title = data.get("title", "")
    description = data.get("description", "")
    return await batch_form_controller.add_batch(current_user, title, description)


@batch_form_router.get("/job-entry/admin/search/batch")
@jwt_required()
async def get_batch():
    current_user = get_jwt_identity()
    data = request.args
    q = data.get("q", "")
    limit = data.get("limit", None)
    per_page = data.get("per_page", "5")
    current_page = data.get("current_page", "0")
    if not q:
        return await batch_form_controller.get_all_batch(
            current_user, limit, per_page, current_page
        )
    else:
        return await batch_form_controller.get_batch_title_id(current_user, q)
