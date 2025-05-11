from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException, Depends

from app.auth.dependencies import get_current_user
from app.auth.schemas import UserSchema
from app.storage.service import background_save_file


storage_router = APIRouter()


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


@storage_router.get("/get_files_list")
async def create_upload_file(curr_user: Annotated[UserSchema, Depends(get_current_user)]):
    pass