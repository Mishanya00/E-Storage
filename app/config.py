import os


ACCESS_JWT_SECRET = os.getenv("ACCESS_JWT_SECRET")
if not ACCESS_JWT_SECRET:
    raise ValueError("ACCESS_JWT_SECRET environment variable is not set")

REFRESH_JWT_SECRET = os.getenv("REFRESH_JWT_SECRET")
if not REFRESH_JWT_SECRET:
    raise ValueError("REFRESH_JWT_SECRET environment variable is not set")

ALGORITHM = os.getenv("ALGORITHM")
if not ALGORITHM:
    raise ValueError("ALGORITHM environment variable is not set")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
if not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES environment variable is not set")

REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
if not REFRESH_TOKEN_EXPIRE_MINUTES:
    raise ValueError("REFRESH_TOKEN_EXPIRE_MINUTES environment variable is not set")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")