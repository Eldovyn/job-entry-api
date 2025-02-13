from sqlalchemy import Column, String, Integer, ForeignKey
from ..database import db
from sqlalchemy.orm import relationship


class UserKrsModel(db.Model):
    __tablename__ = "user_krs"

    krs_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user_form.user_id", ondelete="CASCADE"))
    krs = Column(String, nullable=False)

    user = relationship("UserFormModel", back_populates="user_krs")

    def __init__(self, krs_id, user_id, krs):
        self.krs_id = krs_id
        self.user_id = user_id
        self.krs = krs

    def __repr__(self):
        return f"<UserKrs {self.krs_id!r}>"
