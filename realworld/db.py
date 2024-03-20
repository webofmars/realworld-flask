from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# IN CONTAINER
_ENGINE = create_engine("postgresql+psycopg2://postgres:changeme@postgres/realworld")

# OUTSIDE OF CONTAINER
# _ENGINE = create_engine("postgresql+psycopg2://postgres:changeme@localhost/realworld")

Session = sessionmaker(bind=_ENGINE)


@contextmanager
def get_db_connection():
    """Context manager for handling database transactions."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
        raise e
    finally:
        session.close()
