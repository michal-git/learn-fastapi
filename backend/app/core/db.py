import os
from sqlmodel import SQLModel, create_engine

# Default connection string:
# Using the service name "postgres" from docker-compose, with default credentials.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@postgres:5432/learningplatfrom"
)

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    # Import your models so they are registered with SQLModel's metadata.
    from app.models.exercise import Exercise

    SQLModel.metadata.create_all(engine)
