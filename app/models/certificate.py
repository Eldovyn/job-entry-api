from sqlalchemy import Column, String, Integer, ForeignKey
from ..database import db
from sqlalchemy.orm import relationship
import datetime


class UserCertificateModel(db.Model):
    __tablename__ = "user_certificate"

    certificate_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"))
    certificate = Column(String, nullable=False)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)
    user = relationship("UserFormModel", back_populates="user_certificate")

    def __init__(self, certificate, certificate_id, user_id):
        self.certificate_id = certificate_id
        self.certificate = certificate
        self.user_id = user_id
        self.created_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        self.updated_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    def __repr__(self):
        return f"<UserCertificate {self.certificate_id!r}>"
