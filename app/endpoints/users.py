from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.auth.jwt_authentication import JWTAuthentication
from app.dependencies.database import get_main_db
from app.dependencies.user import get_current_user, get_admin_user
from app.models.entities.users import User
from app.models.schemas.auth.token_data import TokenData
from app.models.schemas.user.user_login import UserLogin
from app.models.schemas.user.user_profile import UserProfile
from app.models.schemas.user.user_signup import UserSignUp

router = APIRouter(prefix='/users')


@router.post("/signup")
async def sign_up(user_info: UserSignUp, db: AsyncIOMotorDatabase = Depends(get_main_db)):
    # TODO: move it to handler or sth, validate basic password rules, add response model, check email, etc
    existing = await db.users.find_one({"username": user_info.username})
    if existing:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {"message": "This user exists! Try other usernames"},
        )

    user_info.password = JWTAuthentication.hash_password(user_info.password)
    user = User.model_validate({**user_info.model_dump(), 'id': None})
    result = await user.insert()
    return JSONResponse(
        {"success": result.acknowledged, "_id": str(result.inserted_id) if result.inserted_id else None},
        status.HTTP_201_CREATED,
    )


@router.post("/login")
async def login(user: UserLogin):
    return await JWTAuthentication().login_with_password(user.username, user.password)


@router.get('/me')
async def profile(user: TokenData = Depends(get_current_user)):
    user = await User.find_by_id(user.id)
    return UserProfile.model_validate(user.model_dump())


@router.get('/list')
async def list_users(user: TokenData = Depends(get_admin_user), db: AsyncIOMotorDatabase = Depends(get_main_db)):
    users = db.users.find({})
    final = []
    for user in await users.to_list(length=100):
        user = User.model_validate({**user, 'id': str(user['_id'])})
        final.append(user.model_dump(exclude={'password'}))

    return final
