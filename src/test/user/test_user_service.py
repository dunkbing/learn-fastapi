from api.user import services as user_services
from sqlalchemy.orm import Session

from test.factories import UserFactory


def test_get_user_by_id(session: Session, user: UserFactory):
    test_user = user_services.get_user_by_id(session, user.id)
    assert test_user.id == user.id
    assert test_user.email == user.email


def test_get_uesr_by_email(session: Session, user: UserFactory):
    test_user = user_services.get_user_by_email(session, user.email)
    assert test_user.id == user.id
    assert test_user.email == user.email
