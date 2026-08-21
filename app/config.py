import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

    FILE_UPLOAD_PATH = os.getenv(
        "FILE_UPLOAD_PATH",
        r"C:\documents\First_docs"
    )

    DB_NAME = os.getenv("DB_NAME", "WEBAPP")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "@Tohid221057")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")