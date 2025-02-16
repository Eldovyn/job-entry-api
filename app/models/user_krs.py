from sqlalchemy import Column, String, Integer, ForeignKey
from ..database import db
from sqlalchemy.orm import relationship


class UserKrsModel(db.Model):
    __tablename__ = "user_krs"

    krs_id = Column(String, primary_key=True)
    user_form_id = Column(
        String,
        ForeignKey("user_form.user_form_id", ondelete="CASCADE"),
        nullable=False,
    )
    krs = Column(String, nullable=False)

    user = relationship("UserFormModel", back_populates="user_krs")

    def __init__(self, krs_id, user_form_id, krs):
        self.krs_id = krs_id
        self.user_form_id = user_form_id
        self.krs = krs

    def __repr__(self):
        return f"<UserKrs {self.krs_id!r}>"
