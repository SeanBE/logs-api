from marshmallow import Schema, fields, post_load

from .base import Base
from app.extensions import db


class SetEntry(Base):
    __table__name = 'set_entry'
    __table_args__ = (db.UniqueConstraint('set_num', 'entry_id',
                                          name='_set_num_entry_uc'),)

    entry_id = db.Column(db.Integer,
                         db.ForeignKey('exercise_entry.id'), nullable=False)

    set_num = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)


class SetEntrySchema(Schema):

    id = fields.Integer(dump_only=True)

    reps = fields.Integer(required=True)
    weight = fields.Integer(allow_none=True)
    comment = fields.String(allow_none=True)

    @post_load
    def make_entry(self, data):
        return SetEntry(**data)
