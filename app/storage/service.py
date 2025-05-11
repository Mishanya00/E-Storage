import shutil
from pathlib import Path

from fastapi import UploadFile


UPLOAD_DIR = Path('/app/storage/uploads') # os.getcwd() returns /app
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def create_email_folder(email: str):
    user_dir = UPLOAD_DIR / email
    user_dir.mkdir(exist_ok=True)


def background_save_file(upload_file: UploadFile, email: str):
    """Wrapper for file-saving (for additional functionality in future)"""
    save_uploaded_file(upload_file, email)


def save_uploaded_file(upload_file: UploadFile, email: str) -> Path:
    file_path = UPLOAD_DIR / email / upload_file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # return file_path