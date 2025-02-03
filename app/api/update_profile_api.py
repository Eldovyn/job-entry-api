from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..controllers import UpdateProfileController

update_profile_router = Blueprint("update_profile_router", __name__)
user_update_profile_controller = UpdateProfileController()


@update_profile_router.patch("/job-entry/update/email")
@jwt_required()
async def update_email():
    current_user = get_jwt_identity()
    data = request.json
    email = data.get("email")
    confirm_email = data.get("confirm_email")
    return await user_update_profile_controller.update_user_email(
        current_user, email, confirm_email
    )


@update_profile_router.patch("/job-entry/update/username")
@jwt_required()
async def update_username():
    current_user = get_jwt_identity()
    data = request.json
    username = data.get("username")
    confirm_username = data.get("confirm_username")
    return await user_update_profile_controller.update_user_username(
        current_user, username, confirm_username
    )


@update_profile_router.patch("/job-entry/update/avatar")
@jwt_required()
async def update_avatar():
    current_user = get_jwt_identity()
    data = request.files
    avatar = data.get("avatar", "")
    return await user_update_profile_controller.update_user_avatar(current_user, avatar)
