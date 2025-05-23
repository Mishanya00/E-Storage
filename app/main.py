from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions import BaseAppException
from app.auth.routes import auth_router
from app.repository.init_db import create_tables
from app.storage.routes import storage_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print('E-Storage app is launched!')

    yield

    print('E-Storage app is shut down!')


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(storage_router, prefix='/storage', tags=['storage'])


@app.exception_handler(BaseAppException)
async def app_exception_handler(request: Request, err: BaseAppException):
    return JSONResponse(
        status_code=err.status_code,
        content={"error": err.message}
    )