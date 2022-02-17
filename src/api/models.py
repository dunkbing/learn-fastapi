from datetime import datetime
from sqlalchemy import Column, DateTime, event


class TimeStampMixin(object):

    create_time = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    update_time = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)
