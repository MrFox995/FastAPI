import psycopg
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg.rows import dict_row
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" # "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

##################################### DB CONNECTION ##################################### 

# Remark: For the actual state of art, this code is useless, since we are using ORM sqlAlchemy instead of write SQL Query inside our Python Code,
#         We stopped updating requests that don't use ORM sqlAlchemy (even if they are still available).

while True:
    try:
        conn = psycopg.connect(host = 'localhost', dbname = 'fastapi', user = 'postgres', password = 'admin', row_factory = dict_row)
        cur = conn.cursor()
        print("DataBase connection was succesfull!")
        break
    except Exception as error:
        print(f"Connecting to DataBase failsed\nError is: {error}")
        time.sleep(2)

##################################### DB CONNECTION ##################################### 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
