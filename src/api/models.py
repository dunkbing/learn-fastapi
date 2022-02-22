from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, event


def camelize(string: str) -> str:

    assert isinstance(string, str), 'Input must be of type str'

    first_alphabetic_character_index = -1
    for index, character in enumerate(string):
        if character.isalpha():
            first_alphabetic_character_index = index
            break

    empty = ''

    if first_alphabetic_character_index == -1:
        return empty

    string = string[first_alphabetic_character_index:]

    titled_string_generator = (
        character for character in string.title() if character.isalnum())

    try:
        return next(titled_string_generator).lower() + empty.join(titled_string_generator)

    except StopIteration:
        return empty


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class TimeStampMixin(object):

    created_time = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_time = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)
