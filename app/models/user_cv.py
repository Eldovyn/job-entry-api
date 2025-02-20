from sqlalchemy import Column, String, Integer, ForeignKey
from ..database import db
from sqlalchemy.orm import relationship


class UserCvModel(db.Model):
    __tablename__ = "user_cv"

    cv_id = Column(String, primary_key=True)
    user_form_id = Column(
        String,
        ForeignKey("user_form.user_form_id", ondelete="CASCADE"),
        nullable=False,
    )
    cv = Column(String, nullable=False)

    user = relationship("UserFormModel", back_populates="user_cv")

    def __init__(self, cv_id, user_form_id, cv):
        self.cv_id = cv_id
        self.user_form_id = user_form_id
        self.cv = cv

    def __repr__(self):
        return f"<UserCv {self.cv_id!r}>"
