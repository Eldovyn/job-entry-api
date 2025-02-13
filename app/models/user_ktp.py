from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import db


class UserKtpModel(db.Model):
    __tablename__ = "user_ktp"

    ktp_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user_form.user_id", ondelete="CASCADE"))
    ktp = Column(String, nullable=False)

    user = relationship("UserFormModel", back_populates="user_ktp")

    def __init__(self, ktp_id, user_id, ktp):
        self.ktp_id = ktp_id
        self.user_id = user_id
        self.ktp = ktp

    def __repr__(self):
        return f"<UserKtp {self.ktp_id!r}>"
