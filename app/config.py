import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

    FILE_UPLOAD_PATH = os.getenv(
        "FILE_UPLOAD_PATH",
        r"C:\documents\First_docs"
    )