from constants.app import SQLITE_DB_URL

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine(SQLITE_DB_URL, echo=True)
Session = sessionmaker(bind=engine)