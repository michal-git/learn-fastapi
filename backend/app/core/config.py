import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

API_V1_STR = "/api/v1"

SECRET_KEY: str = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set. Please add it to your .env file.")

ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
