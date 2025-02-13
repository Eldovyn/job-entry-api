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
    params = request.args
    title = data.get("title", "")
    description = data.get("description", "")
    limit = params.get("limit", None)
    per_page = params.get("per_page", "5")
    current_page = params.get("current_page", "1")
    return await batch_form_controller.add_batch(
        current_user, title, description, limit, per_page, current_page
    )


@batch_form_router.delete("/job-entry/admin/batch")
@jwt_required()
async def delete_batch():
    current_user = get_jwt_identity()
    data = request.json
    params = request.args
    batch_id = data.get("batch_id", "")
    limit = params.get("limit", None)
    per_page = params.get("per_page", "5")
    current_page = params.get("current_page", "1")
    return await batch_form_controller.delete_batch(
        current_user, batch_id, limit, per_page, current_page
    )


@batch_form_router.patch("/job-entry/admin/batch/status")
@jwt_required()
async def update_status_batch():
    current_user = get_jwt_identity()
    data = request.json
    params = request.args
    batch_id = data.get("batch_id", "")
    limit = params.get("limit", None)
    per_page = params.get("per_page", "5")
    current_page = params.get("current_page", "1")
    return await batch_form_controller.update_status_batch(
        current_user,
        batch_id,
        limit,
        per_page,
        current_page,
    )


@batch_form_router.get("/job-entry/admin/search/batch")
@jwt_required()
async def get_admin_batch():
    current_user = get_jwt_identity()
    data = request.args
    q = data.get("q", "")
    limit = data.get("limit", None)
    per_page = data.get("per_page", "5")
    current_page = data.get("current_page", "1")
    if not q:
        return await batch_form_controller.get_all_batch(
            "admin", current_user, limit, per_page, current_page
        )
    else:
        return await batch_form_controller.get_batch_title_id(
            "admin", current_user, q, limit, per_page, current_page
        )


@batch_form_router.get("/job-entry/user/search/batch")
@jwt_required()
async def get_user_batch():
    current_user = get_jwt_identity()
    data = request.args
    q = data.get("q", "")
    limit = data.get("limit", None)
    per_page = data.get("per_page", "5")
    current_page = data.get("current_page", "1")
    if not q:
        return await batch_form_controller.get_all_batch(
            "user", current_user, limit, per_page, current_page
        )
    else:
        return await batch_form_controller.get_batch_title_id(
            "user", current_user, q, limit, per_page, current_page
        )
