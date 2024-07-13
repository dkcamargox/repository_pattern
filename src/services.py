from requests import request
from typing import Dict, Optional
from uuid import UUID

from src.daos import DAO
from models.base import Base
from models.client import Client
from models.source import Source

import json

class ServiceAbstract():
    def __init__(self, entity: str, dao_class: DAO):
        raise NotImplementedError

    def create(self, dao) -> None:
        raise NotImplementedError

    def get_by_id(self, id: UUID) -> DAO:
        raise NotImplementedError


class ApiService(ServiceAbstract):

    base_url: str = None
    
    def __init__(self, entity: str, dao_class: DAO):
        self.base_url = "http://localhost:3000"
        self.authentication_headers = {}
        self.dao_class = dao_class
        self.endpoint = {
            'sources': self.base_url + '/sources',
            'clients': self.base_url + '/clients'
        }[entity]
    
    def create(self, dao: DAO):
        return request(
            url=self.endpoint,
            method='POST',
            headers=self.authentication_headers,
            data=dao.__dict__
        )
    
    def get_by_id(self, id: UUID) -> DAO:
        response = request(
            url=self.endpoint,
            method='GET',
            params={
                'id': id
            },
            headers=self.authentication_headers
        )
        return self.dao_class(**json.loads(response.text))


# THIS CLASS IS NOT PART OF THE DESIGN/ARCHITECTURE IS JUST FOR SQLALCHEMY SERVICE
class SqlAlchemyModels:
    def __init__(self):
        self.source = Source
        self.client = Client
        self.base = Base

    @staticmethod
    def get_models() -> Dict[str, Base]:
        return {
            'sources': Source,
            'clients': Client
        }
    
    def get_model(self, model: str) -> Base:
        return self.get_models()[model]
# END THIS CLASS IS NOT PART OF THE DESIGN/ARCHITECTURE IS JUST FOR SQLALCHEMY SERVICE


class SqlAlchemyService(ServiceAbstract):
    
    engine_string: str = None
    
    def __init__(self, entity: str, dao_class: DAO):
        self.engine_string = "sqlite:///database.sqlite"
        self.models = SqlAlchemyModels()
        self.models.base.set_engine(self.engine_string)
        self.model = self.models.get_model(entity)
        self.dao_class = dao_class
        
    def create(self, dao: DAO):
        self.model(**dao.__dict__).register()
    
    def get_by_id(self, id: UUID) -> DAO:
        return self.dao_class(**self.model.fetch_by_id(id).__dict__)
