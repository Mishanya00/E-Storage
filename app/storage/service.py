import shutil
from pathlib import Path
# from werkzeug.utils import secure_filename # maybe to add for secure filenames


UPLOAD_DIR = Path('/app/storage/uploads') # os.getcwd() returns /app
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def create_email_folder(email: str):
    user_dir = UPLOAD_DIR / email
    user_dir.mkdir(exist_ok=True)


def background_save_file(filename: str, contents: bytes, email: str):
    """Wrapper for file-saving (for additional functionality in future)"""
    save_uploaded_file(filename, contents, email)


def save_uploaded_file(filename: str, contents: bytes, email: str) -> Path:
    file_path = UPLOAD_DIR / email / filename

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    print(f"File {filename} saved to {file_path} for user {email}")
    return file_path