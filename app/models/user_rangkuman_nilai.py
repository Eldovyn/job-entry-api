from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..database import db


class UserRangkumanNilaiModel(db.Model):
    __tablename__ = "user_rangkuman_nilai"

    rangkuman_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user_form.user_id", ondelete="CASCADE"))
    rangkuman = Column(String, nullable=False)

    user = relationship("UserFormModel", back_populates="user_rangkuman_nilai")

    def __init__(self, rangkuman_id, user_id, rangkuman):
        self.rangkuman_id = rangkuman_id
        self.user_id = user_id
        self.rangkuman = rangkuman

    def __repr__(self):
        return f"<UserRangkumanNilai {self.rangkuman_id!r}>"
