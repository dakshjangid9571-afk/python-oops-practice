import os
from pathlib import Path

from dotenv import load_dotenv


CONFIG_DIR = Path(__file__).resolve().parent
load_dotenv(CONFIG_DIR / ".env")


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "student_management"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}
