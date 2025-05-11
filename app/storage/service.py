import os
from pathlib import Path


UPLOAD_DIR = Path('/app/storage/uploads') # os.getcwd() returns /app
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def create_email_folder(email: str):
    email_upload_dir = UPLOAD_DIR / email
    email_upload_dir.mkdir(exist_ok=True)