import os
from sqlmodel import SQLModel, Session, create_engine, select

from app.schemas.exercise import ExerciseType as ExerciseTypeSchema

# Default connection string:
# Using the service name "postgres" from docker-compose, with default credentials.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@postgres:5432/learningplatfrom"
)

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    # Import your models so they are registered with SQLModel's metadata.
    from app.models.user import User
    from app.models.exercise import Exercise, ExerciseType
    from app.models.fill_gap_sentence import FillGapSentence
    from app.models.multiple_choice_question import MultipleChoiceQuestion

    SQLModel.metadata.create_all(engine)

    # Seed default ExerciseType values if they don't already exist.
    with Session(engine) as session:
        exercise_types = session.exec(select(ExerciseType)).all()

        if not exercise_types:
            default_types = [
                ExerciseType(name=ExerciseTypeSchema.FILL_GAP),
                ExerciseType(name=ExerciseTypeSchema.MULTIPLE_CHOICE),
            ]
            session.add_all(default_types)
            session.commit()
