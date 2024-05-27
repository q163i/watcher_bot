# Import Logging
from LoggerConfig import custom_logger
logger = custom_logger()

from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from DefineTables import Users, Admins, BlockedUsers


class TableCreator:
    def __init__(self, engine):
        self.engine = engine
        self.session = sessionmaker(bind=engine)()

    def create_table(self, table_class):
        if not inspect(self.engine).has_table(table_class.__tablename__):
            table_class.__table__.create(bind=self.engine)
            logger.info(f"[DB] Table '{table_class.__tablename__}' created successfully")
        else:
            logger.info(f"[DB] Table '{table_class.__tablename__}' already exists")

    def create_all_tables(self):
        self.create_table(Users)
        self.create_table(Admins)
        self.create_table(BlockedUsers)
        self.session.commit()