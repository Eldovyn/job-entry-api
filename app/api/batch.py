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


@batch_form_router.get("/job-entry/admin/batch")
@jwt_required()
async def get_batch():
    current_user = get_jwt_identity()
    return await batch_form_controller.get_all_batch(current_user)
