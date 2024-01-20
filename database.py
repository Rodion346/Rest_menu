from sqlalchemy import create_engine, MetaData
from models import Base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:1111@localhost/rest"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadate = MetaData()

def creat_Tablesdb():
    Base.metadata.create_all(bind=engine)

def delete_db():
    metadate.reflect(bind=engine)
    metadate.drop_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()