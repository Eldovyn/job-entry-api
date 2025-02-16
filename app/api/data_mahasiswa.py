from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..controllers import DataMahasiswaController

data_mahasiswa_router = Blueprint("data_mahasiswa_router", __name__)


@data_mahasiswa_router.get("/job-entry/batch/data-mahasiswa")
@jwt_required()
async def get_data_mahasiswa():
    current_user = get_jwt_identity()
    data = request.args
    q = data.get("q", "")
    limit = data.get("limit", None)
    per_page = data.get("per_page", "5")
    current_page = data.get("current_page", "1")
    if not q:
        return await DataMahasiswaController.get_all_data_mahasiswa(
            current_user, limit, per_page, current_page
        )
    else:
        return await DataMahasiswaController.get_batch_title_id(
            current_user, q, limit, per_page, current_page
        )
