from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect

from . import models, schemas, settings, utils

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
    saved_user = models.User(
        **new_user.dict()
    ).save()
    return utils.model_schema_intersection(saved_user, schemas.User)
