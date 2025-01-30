from sqlalchemy import Column, String, Integer, ForeignKey
from ..database import db
from sqlalchemy.orm import relationship
import datetime


class UserAvatarModel(db.Model):
    __tablename__ = "user_avatar"

    avatar_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"))
    avatar = Column(String, nullable=False)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)
    user = relationship("UserModel", back_populates="user_avatar")

    def __init__(self, avatar, avatar_id, user_id):
        self.avatar_id = avatar_id
        self.avatar = avatar
        self.user_id = user_id
        self.created_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        self.updated_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    def __repr__(self):
        return f"<UserAvatar {self.avatar_id!r}>"
