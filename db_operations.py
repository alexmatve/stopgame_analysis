from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import Table, Column, create_engine
import os


Base = declarative_base()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(f'postgres+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
Session = sessionmaker(autoflush=True, bind=engine)
session = Session()
