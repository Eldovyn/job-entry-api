from flask import Blueprint, request
from ..controllers import ResetPasswordController

reset_password_router = Blueprint("reset_password_router", __name__)
reset_password_controller = ResetPasswordController()


@reset_password_router.post("/job-entry/reset-password")
async def user_reset_password():
    data = request.json
    email = data.get("email", "")
    return await reset_password_controller.user_reset_password(email)


@reset_password_router.get("/job-entry/reset-password")
async def get_user_reset_password():
    data = request.args
    email = data.get("token", "")
    return await reset_password_controller.get_user_reset_password(email)


@reset_password_router.get("/job-entry/page/reset-password")
async def get_page_user_reset_password():
    data = request.args
    token = data.get("token", "")
    return await reset_password_controller.get_page_user_reset_password(token)


@reset_password_router.patch("/job-entry/user/reset-password")
async def user_update_password():
    params = request.args
    data = request.json
    token = params.get("token", "")
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")
    return await reset_password_controller.user_update_reset_password(
        token, password, confirm_password
    )


@reset_password_router.patch("/job-entry/re-send/reset-password")
async def re_send_user_reset_password():
    data = request.json
    email = data.get("email", "")
    return await reset_password_controller.re_send_user_reset_password(email)
