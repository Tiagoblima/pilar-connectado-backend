from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv
load_dotenv('sql_app/.env')

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URI')
#os.getenv('DATABASE_URI')
print(os.getenv('DATABASE_URI'))

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
