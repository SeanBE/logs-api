from app.extensions import db


class MarshmallowMixin:

    def dump(self):
        return self.__schema__().dump(self)

    @classmethod
    def load(cls, obj):
        return cls.__schema__().load(obj).data

    @classmethod
    def dump_list(cls, object_list):
        return cls.__schema__().dump(object_list, many=True)


class CRUDMixin:

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        try:
            db.session.delete(self)
            return commit and db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return False

    def update(self, commit=True, **kwargs):
        print(kwargs.keys())

        for attr, value in kwargs.items():
            if value is not None:
                setattr(self, attr, value)

        return commit and self.save() or self
