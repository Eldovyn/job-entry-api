from sqlalchemy import Column, String, Integer, Boolean
from ..database import db
from sqlalchemy.orm import relationship
import datetime


class UserModel(db.Model):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        Integer,
        nullable=False,
    )
    updated_at = Column(
        Integer,
        nullable=False,
    )
    account_active = relationship(
        "AccountActiveModel", uselist=False, back_populates="user"
    )
    reset_password = relationship(
        "ResetPasswordModel", uselist=False, back_populates="user"
    )
    user_avatar = relationship("UserAvatarModel", uselist=False, back_populates="user")
    batch_form = relationship("BatchFormModel", uselist=False, back_populates="user")
    is_admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, user_id, username, email, password, created_at):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = created_at

    def __repr__(self):
        return f"<User {self.username!r}>"
