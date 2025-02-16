from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import db


class UserPasFotoModel(db.Model):
    __tablename__ = "user_pas_foto"

    pas_foto_id = Column(String, primary_key=True)
    user_form_id = Column(
        String,
        ForeignKey("user_form.user_form_id", ondelete="CASCADE"),
        nullable=False,
    )
    pas_foto = Column(String, nullable=False)

    user = relationship("UserFormModel", back_populates="user_pas_foto")

    def __init__(self, pas_foto_id, user_form_id, pas_foto):
        self.pas_foto_id = pas_foto_id
        self.user_form_id = user_form_id
        self.pas_foto = pas_foto

    def __repr__(self):
        return f"<UserPasFoto {self.pas_foto_id!r}>"
