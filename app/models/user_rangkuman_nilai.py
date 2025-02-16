from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..database import db


class UserRangkumanNilaiModel(db.Model):
    __tablename__ = "user_rangkuman_nilai"

    rangkuman_nilai_id = Column(String, primary_key=True)
    user_form_id = Column(
        String,
        ForeignKey("user_form.user_form_id", ondelete="CASCADE"),
        nullable=False,
    )
    rangkuman_nilai = Column(String, nullable=False)

    user = relationship("UserFormModel", back_populates="user_rangkuman_nilai")

    def __init__(self, rangkuman_nilai_id, user_form_id, rangkuman_nilai):
        self.rangkuman_nilai_id = rangkuman_nilai_id
        self.user_form_id = user_form_id
        self.rangkuman_nilai = rangkuman_nilai

    def __repr__(self):
        return f"<UserRangkumanNilai {self.rangkuman_nilai_id!r}>"
