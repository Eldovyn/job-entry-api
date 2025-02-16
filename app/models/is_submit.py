from sqlalchemy import Column, String, ForeignKey
from ..database import db
from sqlalchemy.orm import relationship
from ..utils import generate_id


class IsSubmitModel(db.Model):
    __tablename__ = "is_submit"

    submit_id = Column(String, primary_key=True)
    user_form_id = Column(
        String,
        ForeignKey("user_form.user_form_id", ondelete="CASCADE"),
        nullable=False,
    )
    batch_form_id = Column(
        String,
        ForeignKey("batch_form.batch_form_id", ondelete="CASCADE"),
    )
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"))
    token = Column(String, nullable=False)

    user_form = relationship("UserFormModel", back_populates="is_submit")
    batch = relationship("BatchFormModel", back_populates="is_submit")
    user = relationship("UsersModel", back_populates="is_submit")

    def __init__(self, user_form_id, batch_form_id, user_id, token):
        self.user_form_id = user_form_id
        self.batch_form_id = batch_form_id
        self.user_id = user_id
        self.submit_id = generate_id()
        self.token = token

    def __repr__(self):
        return f"<IsSubmit {self.submit_id!r}>"

    def to_dict(self):
        return {
            "submit_id": self.submit_id,
            "user_form_id": self.user_form_id,
            "batch_form_id": self.batch_form_id,
            "token": self.token,
        }
