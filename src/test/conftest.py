import pytest
from fastapi.testclient import TestClient

from . import common
from .factories import UserFactory


@pytest.fixture(scope="session")
def client():
    from api.main import app
    return TestClient(app)


@pytest.fixture(scope="function")
def session():
    # db.begin_nested()
    yield common.session


@pytest.fixture
def user():
    user = UserFactory()
    yield user
    common.session.delete(user)


@pytest.fixture
def users(session):
    return [UserFactory() for i in range(0, 10)]
