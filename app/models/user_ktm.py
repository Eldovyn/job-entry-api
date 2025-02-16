from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import db


class UserKtmModel(db.Model):
    __tablename__ = "user_ktm"

    ktm_id = Column(String, primary_key=True)
    user_form_id = Column(
        String,
        ForeignKey("user_form.user_form_id", ondelete="CASCADE"),
        nullable=False,
    )
    ktm = Column(String, nullable=False)

    user = relationship("UserFormModel", back_populates="user_ktm")

    def __init__(self, ktm_id, user_form_id, ktm):
        self.ktm_id = ktm_id
        self.user_form_id = user_form_id
        self.ktm = ktm
