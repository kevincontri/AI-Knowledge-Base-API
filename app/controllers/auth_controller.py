from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schemas import *
from app.controllers.dependencies import *
from app.exceptions.exceptions import *

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=201)
async def create_user(
    body: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        user = await user_service.create_user(body.username, body.password)
    except DuplicateError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return SingleUserResponse(user=user)


@auth_router.post("/login")
async def login(body: UserLogin, user_service: UserService = Depends(get_user_service)):
    try:
        token = await user_service.verify_user_credentials(body.username, body.password)
        return {"access_token": token, "token_type": "bearer"}

    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
