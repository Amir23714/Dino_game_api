from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

ALCHEMY_URL = "sqlite:///dino_db.db"

engine = create_engine(ALCHEMY_URL)

SessonLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    with SessonLocal() as session:
        yield session


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, index=True, primary_key=True)
    telegram_id = Column(String, index=True, unique=True)
    username = Column(String, index=True)

    status = Column(String, index=True)

    experience = Column(Integer, index=True)

    isAdmin = Column(Boolean, index=True, default=False)


class WorkingUsers(Base):
    __tablename__ = "working_users"
    id = Column(Integer, index=True, primary_key=True)
    telegram_id = Column(String, index=True, unique=True)
    working_status = Column(String, index=True)
    finish = Column(Integer, index=True)
