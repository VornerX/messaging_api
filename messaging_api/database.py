from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from messaging_api.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./messaging_api.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
