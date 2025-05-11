import mimetypes
from pathlib import Path
# from werkzeug.utils import secure_filename # maybe to add for secure filenames

from app.repository.queries import add_file
from app.auth.schemas import UserSchema

UPLOAD_DIR = Path('/app/storage/uploads') # os.getcwd() returns /app
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def create_email_folder(email: str):
    user_dir = UPLOAD_DIR / email
    user_dir.mkdir(exist_ok=True)


async def background_save_file(filename: str, contents: bytes, user: UserSchema):
    """Wrapper for file-saving (for additional functionality in future)"""
    file_path = save_uploaded_file(filename, contents, user.email)
    size = file_path.stat().st_size
    mimetype = mimetypes.guess_type(file_path)[0]

    await add_file(user.user_id, filename, file_path.as_posix(), size, mimetype)


def save_uploaded_file(filename: str, contents: bytes, email: str) -> Path:
    file_path = UPLOAD_DIR / email / filename

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    print(f"File {filename} saved to {file_path} for user {email}")
    return file_path