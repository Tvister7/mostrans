from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)


def init_db() -> None:
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
