from datetime import timedelta

from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from mongoengine import connect

from . import auth, forms, models
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
async def user_create(user_form: forms.UserForm):
    if user_form.is_valid:
        user_new = user_form.save()
        return utils.model_schema_intersection(user_new, schemas.User)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            'text': 'Validation error',
            'errors': user_form.errors,
        }
    )


@app.get("/user", response_model=schemas.User)
async def user_read(current_user: models.User = Depends(auth.get_current_active_user)):
    return utils.model_schema_intersection(current_user, schemas.User)


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


@app.post('/game', status_code=status.HTTP_201_CREATED)
async def game_create(game_form: forms.GameForm):
    if game_form.is_valid:
        game_new = game_form.save()
        return utils.model_schema_intersection(game_new, schemas.Game)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            'text': 'Validation error',
            'errors': game_form.errors,
        }
    )
