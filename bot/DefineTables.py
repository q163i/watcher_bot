# models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

# Define the base class for SQLAlchemy models
Base = declarative_base()

# Define the Users table
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)

# Define the Admins table
class Admins(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    telegram_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Define the BlockedUsers table
class BlockedUsers(Base):
    __tablename__ = 'blockedUsers'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    telegram_id = Column(Integer)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

