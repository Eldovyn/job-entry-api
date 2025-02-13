from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import db


class UserKtmModel(db.Model):
    __tablename__ = "user_ktm"

    ktm_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user_form.user_id", ondelete="CASCADE"))
    ktm = Column(String, nullable=False)

    user = relationship("UserFormModel", back_populates="user_ktm")

    def __init__(self, ktm_id, user_id, ktm):
        self.ktm_id = ktm_id
        self.user_id = user_id
        self.ktm = ktm
