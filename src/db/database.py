from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL: str = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa: E231

metadata: MetaData = MetaData()

Base: declarative_base = declarative_base(metadata=metadata)
engine: create_engine = create_engine(DATABASE_URL)

SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        return db
    finally:
        db.close()
