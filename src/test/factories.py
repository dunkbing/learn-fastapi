from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText

from api.user.models import UserModel
from . import common


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = common.session
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    class Meta:
        model = UserModel

    email = FuzzyText(suffix="@gmail.com", chars=["a", "b", "c"])
    hashed_password = "$2b$12$iekaEoHo4Jnd5Dz2hgaALuqDsEGRWf/tEe3UaNnFwQzSthO1cua6m"
