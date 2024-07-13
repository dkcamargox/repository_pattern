import datetime
import uuid
from typing import Any

import pytz
import sqlalchemy as sqla
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.sql import update


class Base(DeclarativeBase):
    """ "
    Base Model Abstract Class.
    It defines common methods for all models since they all need to perform the same actions.
    It represents a table definition in the database
    """

    __abstract__ = True
    engine = None  # type: ignore
    session = None  # type: ignore

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    
    @classmethod
    def fetch_by_id(cls, id):
        """Searches inside the database for a row with the seeked id.

        Keyword arguments:
        id -- the id of the row it looks for.
        Return: Database Row.
        """
        result = cls.session.query(cls).filter(cls.id == id).one_or_none()
        return result

    @classmethod
    def fetch(cls, **kwargs):
        """Searches inside the database for a row with the seeked tuple of arguments.

        Keyword arguments:
        **kwargs -- the column (name, value) pair of the row it looks for.
        Return: All Database Rows that match the arguments.
        """
        result = cls.session.query(cls).filter_by(**kwargs).all()
        return result

    @classmethod
    def fetch_first(cls, **kwargs):
        """Searches inside the database for the first row with the seeked tuple of arguments

        Keyword arguments:
        **kwargs -- the column (name, value) pair of the row it looks for.
        Return: First Database Rows that match the arguments.
        """
        all_results = cls.fetch(**kwargs)
        return all_results[0] if all_results else None

    def register(self):
        """Given the intanced object writes in the database a Row with the object atributes.

        Return: Instanced object for the registered Database Row.
        """
        try:
            self.session.add(self)
            self.session.commit()
            return self
        except Exception as e:
            print("Error registering the object")
            print(e)
            self.session.rollback()
            return None

    def delete(self):
        """Given the intanced object deteles in the database the object Row.

        Return: Instanced object for the deleted Database Row.
        """
        try:
            self.session.delete(self)
            self.session.commit()
            return self
        except Exception as e:
            print("Error deleting the object")
            print(e)
            self.session.rollback()
            return None

    def update(self, **kwargs):
        """Given the intanced object updates in the database the object Row with the tuple of arguments.

        Keyword arguments:
        **kwargs -- the column (name, value) pair of the row it looks for
        Return: Instanced object for the deleted Database Row.
        """
        if not self._check_kwargs(**kwargs):
            return None
        try:
            stmt = (
                update(type(self))
                .where(type(self).id == self.id)
                .values(updated_at=self.updated_at, **kwargs)
            )
            self.session.execute(stmt)
            self.session.commit()
            self.session.refresh(self)
            return self.fetch_by_id(self.id)
        except Exception as e:
            print("Error updating the object")
            print(e)
            self.session.rollback()
            return None

    def _check_kwargs(self, **kwargs) -> bool:
        """Checks if the tuple of arguments key are a attribute for the instanced object

        **kwargs -- the column (name, value) pair of the row it looks for
        Return: False if one of the kwargs are not an attribute.
        """
        for key in kwargs.keys():
            if key not in [column.key for column in sqla.inspect(self).attrs]:
                return False
        return True

    @classmethod
    def set_engine(cls, connection_string):
        """Changes the engine and the session to a new database connection

        Keyword arguments:
        connection_string -- databse connection link
        """

        cls.engine = sqla.create_engine(connection_string)
        cls.session = sessionmaker(bind=cls.engine)()
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
