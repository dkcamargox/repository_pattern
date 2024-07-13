from typing import Any, Dict
from uuid import UUID, uuid4

class DAO:
    id: UUID
    def __init__(self, **kwargs: dict):
        self.id = uuid4()
        for key, value in kwargs.items():
            if hasattr(self, key):
                self.__setattr__(key, value)


class Client(DAO):
    
    code: str = None
    name:str = None
    status: str = None

    def __init__(
        self,
        code: str,
        name: str,
        status: str,
        **kwargs
    ):
        super().__init__(
            code=code,
            name=name,
            status=status,
            **kwargs
        )
    
    def __repr__(self) -> str:
        return f"""Client(\n\tcode={self.code!r},\n\tname={self.name!r},\n\tstatus={self.status!r}\n)"""


class Source(DAO):

    type: str = None
    name: str = None
    status: str = None
    frequency: str = None
    notes: str = None

    def __init__(
        self,
        type: str,
        name: str,
        status: str,
        frequency: str,
        notes: str,
        **kwargs
    ):
        super().__init__(
            type=type,
            name=name,
            status=status,
            frequency=frequency,
            notes=notes,
            **kwargs
        )
    
    def __repr__(self) -> str:
        return f"""Source(\n\ttype={self.type!r},\n\tname={self.name!r},\n\tstatus={self.status!r}\n)"""

