from .database import Database
from ..models import BatchFormModel, UsersModel, UserFormModel
from ..database import db
import difflib


class BatchDatabase(Database):
    @staticmethod
    async def insert(
        user_id,
        batch_form_id,
        title,
        description,
        created_at,
    ):
        if user := UsersModel.query.filter(UsersModel.user_id == user_id).first():
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
        title = kwargs.get("title")
        limit = kwargs.get("limit")
        role = kwargs.get("role")
        user_id = kwargs.get("user_id")
        if category == "all_batch":
            if role == "admin":
                return BatchFormModel.query.order_by(
                    BatchFormModel.created_at.desc()
                ).all()
            else:
                return (
                    BatchFormModel.query.filter(BatchFormModel.is_active == True)
                    .order_by(BatchFormModel.created_at.desc())
                    .all()
                )
        if category == "batch_id":
            return BatchFormModel.query.filter(
                BatchFormModel.batch_form_id == batch_id
            ).first()
        if category == "form_batch_id":
            if role == "admin":
                return BatchFormModel.query.filter(
                    BatchFormModel.batch_form_id == batch_id
                ).all()
            else:
                return BatchFormModel.query.filter(
                    BatchFormModel.batch_form_id == batch_id,
                    BatchFormModel.is_active == True,
                ).all()
        if category == "title":
            if role == "admin":
                list_batch = BatchFormModel.query.order_by(
                    BatchFormModel.created_at.desc()
                ).all()
            else:
                list_batch = (
                    BatchFormModel.query.filter(BatchFormModel.is_active == True)
                    .order_by(BatchFormModel.created_at.desc())
                    .all()
                )
            titles = [batch.title for batch in list_batch]
            matches = difflib.get_close_matches(title, titles, n=5, cutoff=0.5)
            similar_batchs = (
                BatchFormModel.query.order_by(BatchFormModel.created_at.desc())
                .filter(BatchFormModel.title.in_(matches))
                .limit(limit)
                .all()
            )
            return similar_batchs
        if category == "all_data_mahasiswa":
            return (
                UserFormModel.query.order_by(UserFormModel.created_at.desc())
                .limit(limit)
                .all()
            )
        if category == "title_data_mahasiswa":
            list_mahasiswa = UserFormModel.query.order_by(
                UserFormModel.created_at.desc()
            ).all()
            titles = [mahasiswa.nama for mahasiswa in list_mahasiswa]
            matches = difflib.get_close_matches(title, titles, n=5, cutoff=0.5)
            similar_mahasiswa = (
                UserFormModel.query.order_by(UserFormModel.created_at.desc())
                .filter(UserFormModel.nama.in_(matches))
                .limit(limit)
                .all()
            )
            return similar_mahasiswa
        if category == "data_mahasiswa":
            return UserFormModel.query.filter(UserFormModel.user_id == user_id).first()

    @staticmethod
    async def delete(category, **kwargs):
        batch_id = kwargs.get("batch_id")
        user_id = kwargs.get("user_id")
        if category == "batch_id":
            if data := BatchFormModel.query.filter(
                BatchFormModel.batch_form_id == batch_id
            ).first():
                db.session.delete(data)
                db.session.commit()
                return data
        if category == "data_mahasiswa":
            if data := UserFormModel.query.filter(
                UserFormModel.user_id == user_id
            ).first():
                db.session.delete(data)
                db.session.commit()
                return data

    @staticmethod
    async def update(category, **kwargs):
        batch_id = kwargs.get("batch_id")
        created_at = kwargs.get("created_at")
        if category == "status_batch_id":
            if data := BatchFormModel.query.filter(
                BatchFormModel.batch_form_id == batch_id
            ).first():
                data.is_active = not data.is_active
                data.updated_at = created_at
                db.session.commit()
                return data
