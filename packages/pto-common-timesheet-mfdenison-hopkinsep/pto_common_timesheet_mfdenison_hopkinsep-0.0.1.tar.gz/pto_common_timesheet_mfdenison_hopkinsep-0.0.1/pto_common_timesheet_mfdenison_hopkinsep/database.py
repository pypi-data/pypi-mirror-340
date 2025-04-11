from sqlmodel import create_engine, SQLModel, Session

# Example using SQLite; replace with your production database URI when needed.
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
