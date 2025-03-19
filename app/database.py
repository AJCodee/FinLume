from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL, Connects to the database in postgres/PgAdmin
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:passpost@localhost:5432/FinLume"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Creating database Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()