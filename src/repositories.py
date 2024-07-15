
from src.services import ServiceAbstract, ApiService, SqlAlchemyService
from src.daos import DAO, Source, Client
from uuid import UUID
from abc import ABC, abstractmethod

class RepositoryAbstract(ABC):
    service_class: ServiceAbstract = None
    service: ServiceAbstract = None
    entity: str = None
    dao: DAO = None
    def __init__(self):
        self.service = self.service_class(
            entity=self.entity,
            dao_class=self.dao
        )
    
    # A class that has a metaclass derived from ABCMeta cannot be instantiated unless all of its abstract methods and properties are overridden. 
    @abstractmethod
    def create(self, dao: DAO) -> None:
        return self.service.create(dao=dao)
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> DAO:
        return self.service.get_by_id(id=id)


class SourceRepository(RepositoryAbstract):
    entity: str = "sources"
    dao: DAO = Source


class ClientRepository(RepositoryAbstract):
    entity: str = "clients"
    dao: DAO = Client


class ApiRepository(RepositoryAbstract):
    service_class: ServiceAbstract = ApiService

class ClientApiRepository(ClientRepository, ApiRepository): pass
class SourceApiRepository(SourceRepository, ApiRepository): pass


class SqlAlchemyRepository(RepositoryAbstract):
    service_class: ServiceAbstract = SqlAlchemyService

class ClientSqlAlchemyRepository(ClientRepository, SqlAlchemyRepository): pass
class SourceSqlAlchemyRepository(SourceRepository, SqlAlchemyRepository): pass