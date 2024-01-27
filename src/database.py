from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DB_HOST, DB_PASS, DB_NAME, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()

engine = create_engine(DATABASE_URL)

sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = sessionmaker()
    try:
        yield db
    finally:
        db.close()