from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import db


class UserFormModel(db.Model):
    __tablename__ = "user_form"
    user_form_id = Column(String, primary_key=True)
    user_id = Column(
        String, ForeignKey("users.user_id", ondelete="CASCADE"), unique=True
    )
    batch_form_id = Column(
        String, ForeignKey("batch_form.batch_form_id", ondelete="CASCADE"), unique=True
    )
    nama = Column(String, nullable=False)
    npm = Column(Integer, nullable=False)
    kelas = Column(String, nullable=False)
    tempat_tanggal_lahir = Column(String, nullable=False)
    jenis_kelamin = Column(String, nullable=False)
    alamat = Column(String, nullable=False)
    no_hp = Column(String, nullable=False)
    email = Column(String, nullable=False)
    posisi = Column(String, nullable=False)
    ipk = Column(String, nullable=False)
    created_at = Column(
        Integer,
        nullable=False,
    )

    user = relationship(
        "UsersModel", uselist=False, back_populates="user_form", cascade="all, delete"
    )
    batch = relationship("BatchFormModel", back_populates="user_form")

    def __init__(
        self,
        user_form_id,
        user_id,
        batch_form_id,
        nama,
        npm,
        kelas,
        tempat_tanggal_lahir,
        jenis_kelamin,
        alamat,
        no_hp,
        email,
        posisi,
        ipk,
        created_at,
    ):
        self.user_form_id = user_form_id
        self.user_id = user_id
        self.batch_form_id = batch_form_id
        self.nama = nama
        self.npm = npm
        self.kelas = kelas
        self.tempat_tanggal_lahir = tempat_tanggal_lahir
        self.jenis_kelamin = jenis_kelamin
        self.alamat = alamat
        self.no_hp = no_hp
        self.email = email
        self.posisi = posisi
        self.ipk = ipk
        self.created_at = created_at

    def __repr__(self):
        return f"<UserForm {self.user_form_id}>"
