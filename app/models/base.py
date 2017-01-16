from app.extensions import db
from .mixins import MarshmallowMixin, CRUDMixin


class Base(db.Model, CRUDMixin, MarshmallowMixin):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
