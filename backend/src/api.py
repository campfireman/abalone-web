from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from mongoengine import DoesNotExist, connect

from . import auth, models
from . import operations as op
from . import schemas, settings, utils

connect(
    db=settings.DB_NAME,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    username=settings.DB_USERNAME,
    password=settings.DB_PASSWORD,
    authentication_source='admin',
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def user_create(new_user: schemas.NewUser):
    saved_user = op.user_create(new_user)
    return utils.model_schema_intersection(saved_user, schemas.User)


@app.post('/user/login')
async def user_login(credentials: schemas.UserCredentials):
    user = auth.authenticate(credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
