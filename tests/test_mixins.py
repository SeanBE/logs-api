from unittest import mock
from app.models.mixins import MarshmallowMixin


class User(MarshmallowMixin):

    def __init_(self):
        pass


def test_dump_call():
    User.__schema__ = mock.Mock()

    user = User()
    user.dump()
    user.__schema__().dump.assert_called_once_with(user)


def test_load_call():
    User.__schema__ = mock.Mock()

    user = User()
    User.load({'data': 'data'})
    user.__schema__().load.assert_called_once_with({'data': 'data'})


def test_dump_list_call():
    User.__schema__ = mock.Mock()

    user = User()
    User.dump_list([user])
    user.__schema__().dump.assert_called_once_with([user], many=True)


# # TODO save, delete, update
# from app.extensions import db
# from app.models.mixins import CRUDMixin

# @mock.patch('app.extensions.db')
# def test_save_call(mock_db):
#     # db = mock.Mock()
#     user = User()
#     user.save()
#     print(mock_db.session.mock_calls)
#     mock_db.add.assert_called_once_with(user)
#
#
# # @mock.patch('app.extensions.db')
# def test_save_call():
#     _db = mock.Mock()
#
#     class TestClass(_db.Model, CRUDMixin):
#         def __init__(self):
#             pass
#         # __tablename__ = 'x'
#         # id = _db.Column(db.Integer, primary_key=True)
#
#     user = TestClass()
#     user.save()
#     print(_db.session.mock_calls)
#     _db.add.assert_called_once_with(user)
