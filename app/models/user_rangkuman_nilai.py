from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..database import db


class UserRangkumanNilaiModel(db.Model):
    __tablename__ = "user_rangkuman_nilai"

    rangkuman_id = Column(String, primary_key=True)
    user_form_id = Column(
        String,
        ForeignKey("user_form.user_form_id", ondelete="CASCADE"),
        nullable=False,
    )
    rangkuman = Column(String, nullable=False)

    user = relationship("UserFormModel", back_populates="user_rangkuman_nilai")

    def __init__(self, rangkuman_id, user_form_id, rangkuman):
        self.rangkuman_id = rangkuman_id
        self.user_form_id = user_form_id
        self.rangkuman = rangkuman

    def __repr__(self):
        return f"<UserRangkumanNilai {self.rangkuman_id!r}>"
