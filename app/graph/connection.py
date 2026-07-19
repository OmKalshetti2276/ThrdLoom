from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


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
                NEO4J_URI,
                auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
            )
            self._driver.verify_connectivity()
        return self._driver

    def execute_query(self, query, parameters=None):
        with self.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
        
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