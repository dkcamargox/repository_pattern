from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base



class Source(Base):
    """
    Source Model Class.
    It defines columns for a modeled sources.
    It represents a client data retrieving method (SFTP, Euclid Scraper, etc...) in the database.
    """

    __tablename__ = "sources"
    
    type: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(255))
    frequency: Mapped[str] = mapped_column(String(255))
    notes: Mapped[str] = mapped_column(String(1024), nullable=True)

    def __repr__(self) -> str:
        return f"""Source(\n\ttype={self.type!r},\n\tname={self.name!r},\n\tstatus={self.status!r},\n\tclient={self.client!r},\n\tsweeps={self.sweeps!r}\n)"""
