from flask import jsonify
import os
from werkzeug.datastructures import FileStorage
from ..databases import UserDatabase, BatchDatabase, UserFormDatabase
from ..utils import generate_id
import cloudinary.uploader


class FormController:
    @staticmethod
    async def get_form(role, user_id, batch_id, limit, per_page, current_page):
        errors = {}
        if len(batch_id.strip()) == 0:
            errors["batch_id"] = ["batch_id cannot be empty"]
        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return jsonify({"message": "authorization invalid"}), 401
        if not (
            batch := await BatchDatabase.get(
                "form_batch_id", batch_id=batch_id, role=role
            )
        ):
            return jsonify({"message": "batch not found"}), 404
        per_page = int(per_page) if per_page else 10
        current_page = int(current_page) if current_page else 1

        paginated_data = [
            batch[i : i + per_page] for i in range(0, len(batch), per_page)
        ]
        paginated_batches_dict = [
            [batch.to_dict() for batch in page] for page in paginated_data
        ]

        avatar_url = cloudinary.CloudinaryImage(user.user_avatar.avatar).url
        total_pages = len(paginated_batches_dict)
        current_page = (
            min(current_page, total_pages)
            if current_page <= total_pages
            else total_pages
        )
        paginated_items = (
            paginated_batches_dict[current_page - 1]
            if current_page <= total_pages
            else paginated_batches_dict[-1]
        )

        response_data = {
            "message": "success get all batch",
            "data": [item.to_dict() for item in batch],
            "page": {
                "current_page": current_page,
                "current_batch": paginated_items,
                "total_pages": total_pages,
                "total_items": len(batch),
                "items_per_page": per_page,
                "limit": limit,
                "next_page": current_page + 1 if current_page < total_pages else None,
                "previous_page": current_page - 1 if current_page > 1 else None,
            },
            "user": {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "is_admin": user.is_admin,
                "avatar": avatar_url,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            },
        }

        return jsonify(response_data), 200

    @staticmethod
    async def post_form(
        user_id,
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
    ):
        errors = {}
        if len(batch_id.strip()) == 0:
            errors["batch_id"] = ["batch_id cannot be empty"]
        if len(nama.strip()) == 0:
            errors["nama"] = ["nama cannot be empty"]
        if len(npm.strip()) == 0:
            errors["npm"] = ["npm cannot be empty"]
        if len(kelas.strip()) == 0:
            errors["kelas"] = ["kelas cannot be empty"]
        if len(jurusan.strip()) == 0:
            errors["jurusan"] = ["jurusan cannot be empty"]
        if len(lokasi_kampus.strip()) == 0:
            errors["lokasi_kampus"] = ["lokasi_kampus cannot be empty"]
        if len(tempat_tanggal_lahir.strip()) == 0:
            errors["tempat_tanggal_lahir"] = ["tempat_tanggal_lahir cannot be empty"]
        if len(jenis_kelamin.strip()) == 0:
            errors["jenis_kelamin"] = ["jenis_kelamin cannot be empty"]
        if len(alamat.strip()) == 0:
            errors["alamat"] = ["alamat cannot be empty"]
        if len(no_hp.strip()) == 0:
            errors["no_hp"] = ["no_hp cannot be empty"]
        if len(email.strip()) == 0:
            errors["email"] = ["email cannot be empty"]
        if len(posisi.strip()) == 0:
            errors["posisi"] = ["posisi cannot be empty"]
        if len(ipk.strip()) == 0:
            errors["ipk"] = ["ipk cannot be empty"]

        VALID_EXTENSIONS = [".pdf"]
        MAX_FILE_SIZE = 500 * 1024

        if isinstance(cv, FileStorage):

            _, ext = os.path.splitext(cv.filename)
            if ext.lower() not in VALID_EXTENSIONS:
                errors.setdefault("cv", []).append("Only accept jpeg/png/jpg/pdf")

            file_content_cv = cv.read()
            if len(file_content_cv) > MAX_FILE_SIZE:
                errors.setdefault("cv", []).append("File is too large")

            if len(file_content_cv) == 0:
                errors.setdefault("cv", []).append("File is empty")

        if isinstance(ktm, FileStorage):

            _, ext = os.path.splitext(ktm.filename)
            if ext.lower() not in VALID_EXTENSIONS:
                errors.setdefault("ktm", []).append("Only accept jpeg/png/jpg/pdf")

            file_content_ktm = ktm.read()
            if len(file_content_ktm) > MAX_FILE_SIZE:
                errors.setdefault("ktm", []).append("File is too large")

            if len(file_content_ktm) == 0:
                errors.setdefault("ktm", []).append("File is empty")

        if isinstance(krs, FileStorage):

            _, ext = os.path.splitext(krs.filename)
            if ext.lower() not in VALID_EXTENSIONS:
                errors.setdefault("krs", []).append("Only accept jpeg/png/jpg/pdf")

            file_content_krs = krs.read()
            if len(file_content_krs) > MAX_FILE_SIZE:
                errors.setdefault("krs", []).append("File is too large")

            if len(file_content_krs) == 0:
                errors.setdefault("krs", []).append("File is empty")

        if isinstance(pas_foto, FileStorage):

            _, ext = os.path.splitext(pas_foto.filename)
            if ext.lower() not in VALID_EXTENSIONS:
                errors.setdefault("pas_foto", []).append("Only accept jpeg/png/jpg/pdf")

            file_content_pas_foto = pas_foto.read()
            if len(file_content_pas_foto) > MAX_FILE_SIZE:
                errors.setdefault("pas_foto", []).append("File is too large")

            if len(file_content_pas_foto) == 0:
                errors.setdefault("pas_foto", []).append("File is empty")

        if isinstance(ktp, FileStorage):

            _, ext = os.path.splitext(ktp.filename)
            if ext.lower() not in VALID_EXTENSIONS:
                errors.setdefault("ktp", []).append("Only accept jpeg/png/jpg/pdf")

            file_content_ktp = ktp.read()
            if len(file_content_ktp) > MAX_FILE_SIZE:
                errors.setdefault("ktp", []).append("File is too large")

            if len(file_content_ktp) == 0:
                errors.setdefault("ktp", []).append("File is empty")

        if isinstance(rangkuman_nilai, FileStorage):

            _, ext = os.path.splitext(rangkuman_nilai.filename)
            if ext.lower() not in VALID_EXTENSIONS:
                errors.setdefault("rangkuman_nilai", []).append(
                    "Only accept jpeg/png/jpg/pdf"
                )

            file_content_rangkuman_nilai = rangkuman_nilai.read()
            if len(file_content_rangkuman_nilai) > MAX_FILE_SIZE:
                errors.setdefault("rangkuman_nilai", []).append("File is too large")

            if len(file_content_rangkuman_nilai) == 0:
                errors.setdefault("rangkuman_nilai", []).append("File is empty")

        if certificate and isinstance(certificate, FileStorage):
            _, ext = os.path.splitext(certificate.filename)
            if ext.lower() not in VALID_EXTENSIONS:
                errors.setdefault("certificate", []).append(
                    "Only accept jpeg/png/jpg/pdf"
                )

            file_content_certificate = certificate.read()
            if len(file_content_certificate) > MAX_FILE_SIZE:
                errors.setdefault("certificate", []).append("File is too large")

            if len(file_content_certificate) == 0:
                errors.setdefault("certificate", []).append("File is empty")

        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400

        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return jsonify({"message": "authorization invalid"}), 401

        cv.seek(0)
        user_cv = cloudinary.uploader.upload(cv, folder="cv/")
        user_cv_id = generate_id()

        ktm.seek(0)
        user_ktm = cloudinary.uploader.upload(ktm, folder="ktm/")
        user_ktm_id = generate_id()

        krs.seek(0)
        user_krs = cloudinary.uploader.upload(krs, folder="krs/")
        user_krs_id = generate_id()

        pas_foto.seek(0)
        user_pas_foto = cloudinary.uploader.upload(pas_foto, folder="pas_foto/")
        user_pas_foto_id = generate_id()

        ktp.seek(0)
        user_ktp = cloudinary.uploader.upload(ktp, folder="ktp/")
        user_ktp_id = generate_id()

        rangkuman_nilai.seek(0)
        user_rangkuman_nilai = cloudinary.uploader.upload(
            rangkuman_nilai, folder="rangkuman_nilai/"
        )
        user_rangkuman_nilai_id = generate_id()

        user_certificate_id = generate_id() if certificate else None
        user_certificate = None
        if certificate:
            certificate.seek(0)
            user_certificate = cloudinary.uploader.upload(
                certificate, folder="certificate/"
            )

        user_form_id = generate_id()

        if submit_form := await UserFormDatabase.get(
            "is_submit", user_form_id=user_form_id
        ):
            return jsonify({"message": "form already submitted"}), 409

        if not (
            batch_form := await UserFormDatabase.insert(
                user_id,
                batch_id,
                user_form_id,
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
                user_cv["asset_id"],
                user_cv_id,
                user_ktm["asset_id"],
                user_ktm_id,
                user_krs["asset_id"],
                user_krs_id,
                user_pas_foto["asset_id"],
                user_pas_foto_id,
                user_ktp["asset_id"],
                user_ktp_id,
                user_rangkuman_nilai["asset_id"],
                user_rangkuman_nilai_id,
                (
                    user_certificate
                    if not user_certificate
                    else user_certificate["asset_id"]
                ),
                user_certificate_id,
            )
        ):
            return jsonify({"message": "batch not found"}), 404

        return jsonify({"message": "success post form"}), 201
