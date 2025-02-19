from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..controllers import DataMahasiswaController

data_mahasiswa_router = Blueprint("data_mahasiswa_router", __name__)


@data_mahasiswa_router.get("/job-entry/data-mahasiswa")
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
            False, current_user, limit, per_page, current_page
        )
    else:
        return await DataMahasiswaController.get_data_mahasiswa_title_id(
            False, current_user, q, limit, per_page, current_page
        )


@data_mahasiswa_router.get("/job-entry/export/data-mahasiswa")
@jwt_required()
async def get_export_data_mahasiswa():
    current_user = get_jwt_identity()
    data = request.args
    q = data.get("q", "")
    limit = data.get("limit", None)
    per_page = data.get("per_page", "5")
    current_page = data.get("current_page", "1")
    if not q:
        return await DataMahasiswaController.get_all_data_mahasiswa(
            True, current_user, limit, per_page, current_page
        )
    else:
        return await DataMahasiswaController.get_data_mahasiswa_title_id(
            True, current_user, q, limit, per_page, current_page
        )


@data_mahasiswa_router.delete("/job-entry/data-mahasiswa")
@jwt_required()
async def delete_data_mahasiswa():
    current_user = get_jwt_identity()
    data = request.args
    json = request.json
    limit = data.get("limit", None)
    per_page = data.get("per_page", "5")
    current_page = data.get("current_page", "1")
    target_user_id = json.get("target_user_id", "")
    return await DataMahasiswaController.delete_data_mahasiswa(
        current_user, limit, per_page, current_page, target_user_id
    )
