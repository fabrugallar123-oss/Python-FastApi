
from sqlmodel import SQLModel, create_engine, Session


url = "sqlite:///./base_db.db"

engine = create_engine(url, connect_args = {"check_same_thread":False})


def get_db():
    with Session(engine) as session:
        yield session