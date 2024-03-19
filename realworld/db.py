from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Assuming you have your database URI stored in a variable
# _ENGINE = create_engine("postgresql+psycopg2://postgres:changeme@localhost/realworld")
_ENGINE = create_engine("postgresql+psycopg2://postgres:changeme@postgres/realworld")
Session = sessionmaker(bind=_ENGINE)


@contextmanager
def create_db_transaction():
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
