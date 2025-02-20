from flask import Blueprint, request
from ..controllers import UserController
from flask_jwt_extended import jwt_required, get_jwt_identity

me_router = Blueprint("me_router", __name__)
user_controller = UserController()


@me_router.get("/job-entry/@me")
@jwt_required()
async def user_me():
    current_user = get_jwt_identity()
    return await user_controller.user_me(current_user)
