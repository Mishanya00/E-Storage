from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class FileSchema(BaseModel):
    file_id: Annotated[int, Field(ge=0)]
    user_id: Annotated[int, Field(ge=0)]
    filename: str
    path: str
    size: int
    mime_type: str
    upload_time: datetime