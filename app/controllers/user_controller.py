from fastapi import APIRouter, HTTPException, Depends, Path
from app.schemas.user_schemas import *
from app.controllers.dependencies import *
from app.exceptions.exceptions import *

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.post("", status_code=201)
async def create_user(body: UserCreate, user_service: UserService = Depends(get_user_service)):
    try:
        user = await user_service.create_user(body.username)
    except DuplicateError as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
        )
    return SingleUserResponse(user=user)

@user_router.get("", status_code=200)
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_all_users()
    return MultipleUserResponse(count=len(users), users=users)


@user_router.get("/{user_id}", status_code=200)
async def get_user_by_id(
    user_id: int = Path(..., gt=0), 
    user_service: UserService = Depends(get_user_service)
    ):
    try:
        user = await user_service.get_user_by_id(user_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    return SingleUserResponse(user=user)

