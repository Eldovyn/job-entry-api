from .database import Database
from ..models import (
    UserFormModel,
    UsersModel,
    UserKtmModel,
    UserPasFotoModel,
    UserKrsModel,
    UserKtpModel,
    UserCertificateModel,
    UserRangkumanNilaiModel,
    UsersModel,
    BatchFormModel,
    UserCvModel,
)
import datetime
from ..database import db


class UserFormDatabase(Database):
    @staticmethod
    async def insert(
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
        cv,
        cv_id,
        ktm,
        ktm_id,
        krs,
        krs_id,
        pas_foto,
        pas_foto_id,
        ktp,
        ktp_id,
        rangkuman_nilai,
        rangkuman_nilai_id,
        certificate,
        certificate_id,
    ):
        if user_data := UsersModel.query.filter(UsersModel.user_id == user_id).first():
            if batch_data := BatchFormModel.query.filter(
                BatchFormModel.batch_form_id == batch_id
            ).first():
                user_form = UserFormModel(
                    user_form_id=user_form_id,
                    user_id=user_id,
                    batch_form_id=batch_id,
                    nama=nama,
                    npm=npm,
                    kelas=kelas,
                    jurusan=jurusan,
                    lokasi_kampus=lokasi_kampus,
                    tempat_tanggal_lahir=tempat_tanggal_lahir,
                    jenis_kelamin=jenis_kelamin,
                    alamat=alamat,
                    no_hp=no_hp,
                    email=email,
                    posisi=posisi,
                    ipk=ipk,
                    created_at=datetime.datetime.now(datetime.timezone.utc).timestamp(),
                )
                user_cv = UserCvModel(cv_id, user_id, cv)
                user_ktm = UserKtmModel(ktm_id, user_id, ktm)
                user_krs = UserKrsModel(krs_id, user_id, krs)
                user_pas_foto = UserPasFotoModel(pas_foto_id, user_id, pas_foto)
                user_ktp = UserKtpModel(ktp_id, user_id, ktp)
                user_rangkuman_nilai = UserRangkumanNilaiModel(
                    rangkuman_nilai_id, user_id, rangkuman_nilai
                )
                user_certificate = (
                    UserCertificateModel(certificate_id, user_id, certificate)
                    if certificate
                    else None
                )
                db.session.add(user_form)
                db.session.add(user_cv)
                db.session.add(user_ktm)
                db.session.add(user_krs)
                db.session.add(user_pas_foto)
                db.session.add(user_ktp)
                db.session.add(user_pas_foto)
                db.session.add(user_rangkuman_nilai)
                if user_certificate:
                    db.session.add(user_certificate)
                db.session.commit()
                return user_form

    @staticmethod
    async def get(category, **kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        pass

    @staticmethod
    async def update(category, **kwargs):
        pass
