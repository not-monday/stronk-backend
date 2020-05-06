import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def get_test_db_session():
    """Creates a DB session for testing."""
    db_url = os.getenv("TEST_DATABASE_URL")
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()


def close_session(session):
    """Close database session."""
    session.close()


def execute(session, path):
    """Executes SQL file located at the path with the database session."""
    conn = session.connection()
    with open(path) as file:
        queries = file.read()
        conn.execute(queries)
        session.commit()
