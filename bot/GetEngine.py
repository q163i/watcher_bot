# GetEngine.py

# Import Logging
from LoggerConfig import custom_logger
logger = custom_logger()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_NAME


class Database:
    def __init__(self):
        self.engine = self.get_engine()
        self.Session = self.get_session()

    def get_engine(self):
        return create_engine(f'sqlite:///{DB_NAME}')

    def get_session(self):
        return sessionmaker(bind=self.engine)