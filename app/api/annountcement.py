from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..controllers import AnnountcementController

annountcement_router = Blueprint("annountcement_router", __name__)


@annountcement_router.post("/job-entry/annountcement")
@jwt_required()
async def annountcement_post():
    json = request.json
    title = json.get("title", "")
    content = json.get("content", "")
    current_user = get_jwt_identity()
    return await AnnountcementController().annountcement_post(
        current_user, title, content
    )
