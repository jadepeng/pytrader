from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self):
        SQLALCHEMY_DATABASE_URL = f'sqlite:///pytrader.db'
        self.engine = create_engine(
            SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
        )

        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, expire_on_commit=False, bind=self.engine
        )

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_session(self):
        return self.SessionLocal()

    def execute_sql(self, statement):
        with self.engine.connect() as conn:
            conn.execute(statement)


Base = declarative_base()

