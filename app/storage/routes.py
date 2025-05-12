import re
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse

from app.auth.dependencies import get_current_user
from app.auth.schemas import UserSchema
from app.storage.service import background_save_file
from app.repository import queries
from app.storage.schemas import FileSchema


storage_router = APIRouter()

ALLOWED_FILENAME_PATTERN = r'^[a-zA-Z0-9_\-\.]+$'


@storage_router.post("/upload_file")
async def upload_file(background_tasks: BackgroundTasks,
                             curr_user: Annotated[UserSchema, Depends(get_current_user)],
                             file: Annotated[UploadFile, File()]):
    if not file:
        return {"message": "No upload file sent"}
    if not file.filename:
         raise HTTPException(status_code=400, detail="File has no filename")
    else:
        try:
            file_contents = await file.read()
            original_filename = file.filename

            background_tasks.add_task(
                background_save_file,
                filename=original_filename,
                contents=file_contents,
                user=curr_user
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
        finally:
            await file.close()
            return {"message": f"file {file.filename} has been added to upload queue."}


@storage_router.get("/get_files")
async def get_files(curr_user: Annotated[UserSchema, Depends(get_current_user)]):
    records = await queries.get_files_by_user(curr_user.user_id)
    files = []

    for record in records:
        files.append(FileSchema(**record))

    return files


@storage_router.get("/get_file")
async def get_file(curr_user: Annotated[UserSchema, Depends(get_current_user)]):
    pass


@storage_router.delete("/delete_file")
async def delete_file(curr_user: Annotated[UserSchema, Depends(get_current_user)]):
    pass


@storage_router.put("/change_filename")
async def change_filename(curr_user: Annotated[UserSchema, Depends(get_current_user)]):
    pass