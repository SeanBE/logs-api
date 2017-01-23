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
