from .database import Database
from ..models import AnnountcementModel
from ..database import db


class AnnountcementDatabase(Database):
    @staticmethod
    async def insert(annountcement_id, user_id, title, content):
        data = AnnountcementModel(annountcement_id, user_id, title, content)
        db.session.add(data)
        db.session.commit()
        return data

    @staticmethod
    async def get(category, **kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        pass

    @staticmethod
    async def update(category, **kwargs):
        pass
