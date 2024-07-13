from typing import TYPE_CHECKING, List

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

class Client(Base):
    """
    Client Model Class.
    It defines columns for a modeled clients.
    It represents a client on the database.
    """

    __tablename__ = "clients"

    code: Mapped[str] = mapped_column(
        String(255), index=True, unique=True, nullable=True
    )
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(255), index=True)

    def __repr__(self) -> str:
        return f"""Client(\n\tcode={self.code!r},\n\tname={self.name!r},\n\tstatus={self.status!r}\n)"""
