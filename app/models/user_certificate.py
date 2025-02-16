from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..database import db


class UserCertificateModel(db.Model):
    __tablename__ = "user_certificate"

    certificate_id = Column(String, primary_key=True)
    user_form_id = Column(
        String,
        ForeignKey("user_form.user_form_id", ondelete="CASCADE"),
        nullable=False,
    )
    certificate = Column(String, nullable=False)

    user = relationship("UserFormModel", back_populates="user_certificate")

    def __init__(self, certificate_id, user_form_id, certificate):
        self.certificate_id = certificate_id
        self.user_form_id = user_form_id
        self.certificate = certificate

    def __repr__(self):
        return f"<UserCertificate {self.certificate_id!r}>"
