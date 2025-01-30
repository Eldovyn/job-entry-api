from flask import Blueprint, request
from ..controllers import UserController
import cloudinary
from ..config import avatar_id

register_router = Blueprint("register_router", __name__)
user_controller = UserController()


@register_router.post("/job-entry/register")
async def user_register():
    data = request.json
    email = data.get("email", "")
    username = data.get("username", "")
    password = data.get("password", "")
    avatar = cloudinary.CloudinaryImage(avatar_id).public_id
    return await UserController().user_register(email, username, password, avatar)
