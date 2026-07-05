from neo4j import GraphDatabase
from src.config import config


class GraphDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._driver = None
        return cls._instance

    def connect(self):
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                config.neo4j_uri,
                auth=(config.neo4j_user, config.neo4j_password),
            )
            self._driver.verify_connectivity()
        return self._driver

    @property
    def driver(self):
        if self._driver is None:
            return self.connect()
        return self._driver

    def close(self):
        if self._driver is not None:
            self._driver.close()
            self._driver = None

    def session(self):
        return self.driver.session()


db = GraphDB()
