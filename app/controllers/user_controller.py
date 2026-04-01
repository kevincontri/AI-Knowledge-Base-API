from fastapi import APIRouter, HTTPException
from app.schemas.user_schemas import *
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from fastapi.responses import JSONResponse
from app.controllers.json_output import *

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

user_service = UserService(UserRepository())

@user_router.post("/")
async def create_user(body: UserCreate):
    try:
        user = await user_service.create_user(body.username)
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
        )
        
    user_formatted = format_single_user(user)
    
    if not user_formatted:
        raise HTTPException(
            status_code=400, 
            detail="User not created"
            )
        
    return JSONResponse(
        content=user_formatted,
        status_code=201
    )

@user_router.get("/")
async def get_all_users():
    users = await user_service.get_all_users()
    users_formatted = format_multiple_users(users)
    
    return JSONResponse(
        content=users_formatted,
        status_code=200
    )

@user_router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    try:
        user = await user_service.get_user_by_id(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found"
        )
        
    user_formatted = format_single_user(user)
    
    return JSONResponse(
        content=user_formatted,
        status_code=200
    )
