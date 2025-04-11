from doorbeen.core.connections.clients.factory.abstracts import DatabaseClientFactory
from doorbeen.core.types.ts_model import TSModel


class DatabaseClientGenerator(TSModel):

    def parse(self, factory: DatabaseClientFactory, credentials: TSModel, **kwargs) -> TSModel:
        creds = factory.create_client(credentials=credentials, **kwargs)
        return creds

