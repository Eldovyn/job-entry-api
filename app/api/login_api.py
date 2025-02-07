from flask import Blueprint, request
from ..controllers import UserController

login_router = Blueprint("login_router", __name__)
user_controller = UserController()


@login_router.post("/job-entry/login")
async def user_login():
    data = request.json
    email = data.get("email", "")
    password = data.get("password", "")
    return await user_controller.user_login(email, password)
