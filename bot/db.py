# Import Logging
from LoggerConfig import custom_logger
logger = custom_logger()

# Import necessary modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DefineTables import Users

from sqlalchemy.ext.declarative import declarative_base
from config import DB_USER, DB_PASSWORD, DB_NAME, ALLOWED_USERS

# Define the base class for SQLAlchemy models
Base = declarative_base()

# Create the SQLAlchemy engine
engine = create_engine(f'sqlite:///{DB_NAME}')

# Create the SQLAlchemy session
Session = sessionmaker(bind=engine)
session = Session()

# Function to create the database
def database():
    logger.info("[System] Create database")
    # Import the TableCreator class
    from TableCreator import TableCreator
    # Create an instance of TableCreator
    table_creator = TableCreator(engine)
    # Create all tables
    table_creator.create_all_tables()

    # Create a new user
    new_user = Users(name=DB_USER, password=DB_PASSWORD, email='tech_user@example.com')
    # Add the new user to the session
    session.add(new_user)
    # Commit the session
    session.commit()
    logger.info(f"[DB] Add default user: '{DB_USER}' in table 'users'")


    # Import the AdminImporter class
    logger.info("[DB] Import users from ALLOWED_USERS env to admins..")
    from AdminImport import AdminImporter
    # Create an instance of AdminImporter
    admin_importer = AdminImporter(engine, ALLOWED_USERS)
    # Import admins
    admin_importer.import_admins()

    logger.info("[DB] Checking users in databases")
    # Import the check_list class
    from TableCheck import check_list
    # Create an instance of check_list
    checker = check_list(session)
    # Check all tables
    checker.check_all()
