from src.repositories import *
from src.daos import Client, Source
from uuid import UUID
def main():

    client_repository = ClientApiRepository()
    source_repository = SourceApiRepository()
    client_repository = ClientSqlAlchemyRepository()
    source_repository = SourceSqlAlchemyRepository()

    comph88 = Client(
        code="comph88",
        name="Compass Health",
        status="pending"
    )
    client_repository.create(comph88)
    print(client_repository.get_by_id(UUID('fec7eb77d3404a90b519d606c863536d')))

    zirmed = Source(
        type="scraper",
        name="zirmed",
        status="disabled",
        notes="",
        frequency="adhoc"
    )
    source_repository.create(zirmed)
    print(source_repository.get_by_id(id=UUID("a28da29c9b7b4ae79af4345b88571389")))





if __name__ == '__main__':
    main()