from sqlalchemy import Column, String, ForeignKey, Text, Boolean
from ..database import db
from sqlalchemy.orm import relationship


class AnnountcementModel(db.Model):
    __tablename__ = "announcement"

    annountcement_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_visible = Column(Boolean, nullable=False, default=True)

    user = relationship("UsersModel", back_populates="announcement")

    def __init__(self, annountcement_id, user_id, title, content):
        self.annountcement_id = annountcement_id
        self.user_id = user_id
        self.title = title
        self.content = content

    def __repr__(self):
        return f"<Annountcement {self.annountcement_id!r}>"

    def to_dict(self):
        return {
            "annountcement_id": self.annountcement_id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
        }
