from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import db


class BatchFormModel(db.Model):
    __tablename__ = "batch_form"
    batch_form_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(
        Integer,
        nullable=False,
    )
    updated_at = Column(
        Integer,
        nullable=False,
    )
    is_active = Column(Boolean, nullable=False, default=True)
    user = relationship("UserModel", back_populates="batch_form")

    def __init__(
        self,
        batch_form_id,
        user_id,
        title,
        description,
        created_at,
        updated_at,
    ):
        self.batch_form_id = batch_form_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Batch {self.batch_form_id}>"

    def to_dict(self):
        return {
            "batch_id": self.batch_form_id,
            "user_id": self.user_id,
            "author": self.user.username,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
        }
