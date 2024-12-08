from sqlmodel import SQLModel, Session, create_engine

# SQLite Database
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/kowan-inventory"

engine = create_engine(DATABASE_URL, echo=True)

# Create database tables
def init_db():
    SQLModel.metadata.create_all(engine)

# Dependency for database session
def get_db():
    with Session(engine) as session:
        yield session
