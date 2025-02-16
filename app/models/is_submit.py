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

    batch_form = relationship("UserFormModel", back_populates="is_submit")

    def __init__(self, user_form_id):
        self.user_form_id = user_form_id
        self.submit_id = generate_id()

    def __repr__(self):
        return f"<IsSubmit {self.submit_id!r}>"
