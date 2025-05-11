from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException, Depends

from app.auth.dependencies import get_current_user
from app.auth.schemas import UserSchema


storage_router = APIRouter()


@storage_router.post("/uploadfile")
async def create_upload_file(background_tasks: BackgroundTasks,
                             curr_user: Annotated[UserSchema, Depends(get_current_user)],
                             file: Annotated[UploadFile, File()]):
    if not file:
        return {"message": "No upload file sent"}
    if not file.filename:
         raise HTTPException(status_code=400, detail="File has no filename")
    else:
        try:
            pass
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
        finally:
            pass
            # await file.close()

        return {"message": f"file {file.filename} has been successfully uploaded."}