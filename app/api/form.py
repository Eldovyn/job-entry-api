from flask import Blueprint, request, jsonify
from ..controllers import FormController
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

form_router = Blueprint("form_router", __name__)


@form_router.get("/job-entry/form")
@jwt_required()
async def get_form():
    current_user = get_jwt_identity()
    data = request.args
    q = data.get("q", "")
    claims = get_jwt()
    if not "is_admin" in claims:
        return jsonify({"message": "authorization invalid"}), 401
    is_admin = claims["is_admin"]
    return await FormController.get_form(
        "user" if not is_admin else "admin", current_user, q, None, "5", "1"
    )


@form_router.get("/job-entry/form/is-submitted")
@jwt_required()
async def get_form_is_submitted():
    current_user = get_jwt_identity()
    data = request.args
    q = data.get("q", "")
    return await FormController.get_form_is_submit(current_user, q)


@form_router.post("/job-entry/form")
@jwt_required()
async def add_form():
    current_user = get_jwt_identity()
    data = request.form
    params = request.args
    files = request.files
    batch_id = params.get("batch_id", "")
    nama = data.get("nama", "")
    npm = data.get("npm", "")
    kelas = data.get("kelas", "")
    jurusan = data.get("jurusan", "")
    lokasi_kampus = data.get("lokasi_kampus", "")
    tempat_tanggal_lahir = data.get("tempat_tanggal_lahir", "")
    jenis_kelamin = data.get("jenis_kelamin", "")
    alamat = data.get("alamat", "")
    no_hp = data.get("no_hp", "")
    email = data.get("email", "")
    posisi = data.get("posisi", "")
    ipk = data.get("ipk", "")
    cv = files.get("cv", None)
    ktm = files.get("ktm", None)
    krs = files.get("krs", None)
    pas_foto = files.get("pas_foto", None)
    ktp = files.get("ktp", None)
    rangkuman_nilai = files.get("rangkuman_nilai", None)
    certificate = files.get("certificate", None)
    return await FormController.post_form(
        current_user,
        batch_id,
        nama,
        npm,
        kelas,
        jurusan,
        lokasi_kampus,
        tempat_tanggal_lahir,
        jenis_kelamin,
        alamat,
        no_hp,
        email,
        posisi,
        ipk,
        cv,
        ktm,
        krs,
        pas_foto,
        ktp,
        rangkuman_nilai,
        certificate,
    )
