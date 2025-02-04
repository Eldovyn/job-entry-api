from .database import Database
from ..models import BatchFormModel, UserModel
from ..database import db


class BatchDatabase(Database):
    @staticmethod
    async def insert(
        user_id,
        batch_form_id,
        title,
        description,
        created_at,
    ):
        if user := UserModel.query.filter(UserModel.user_id == user_id).first():
            batch_data = BatchFormModel(
                batch_form_id=batch_form_id,
                user_id=user.user_id,
                title=title,
                description=description,
                created_at=created_at,
                updated_at=created_at,
            )
            db.session.add(batch_data)
            db.session.commit()
            return batch_data

    @staticmethod
    async def get(category, **kwargs):
        batch_id = kwargs.get("batch_id")
        if category == "all_batch":
            return BatchFormModel.query.order_by(BatchFormModel.created_at.desc()).all()
        if category == "batch_id":
            return BatchFormModel.query.filter(
                BatchFormModel.batch_form_id == batch_id
            ).first()

    @staticmethod
    async def delete(category, **kwargs):
        pass

    @staticmethod
    async def update(category, **kwargs):
        pass
