from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Create the SQLAlchemy engine using the URL from our config
engine = create_engine(settings.DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the base class our database models will inherit from
Base = declarative_base()

# Dependency function to use in FastAPI endpoints
def get_db():
    """Yields a database session and safely closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
