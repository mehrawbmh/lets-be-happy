from fastapi import FastAPI, Depends, status, APIRouter
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.results import InsertOneResult

from app.core.auth.jwt_authentication import JWTAuthentication
from app.dependencies.database import get_main_db
from app.dependencies.user import get_current_user
from app.models.entities.users import User
from app.models.schemas.auth.token_data import TokenData
from app.models.schemas.user.user_login import UserLogin
from app.models.schemas.user.user_profile import UserProfile
from app.models.schemas.user.user_signup import UserSignUp

app = FastAPI()
router = APIRouter(prefix='/api')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.get("/")
async def root():
    return {"message": "Let's be happy."}


@router.get("/hello/{name}")
async def health_test(name: str, message: str = '', db: AsyncIOMotorDatabase = Depends(get_main_db)):
    test_recode = await db.users.find_one({})
    print('test:', test_recode, sep=' ')
    message = 'you said ' + message if message else ''

    resp = {
        'message': f"Hello {name}. It's working bro ^_^. {message}"
    }
    response = JSONResponse(resp, 200)

    return response


@router.post("/users/signup")
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
    result: InsertOneResult = await db.users.insert_one(user.model_dump(exclude={'id'}))
    return JSONResponse(
        {"success": result.acknowledged, "_id": str(result.inserted_id) if result.inserted_id else None},
        status.HTTP_201_CREATED,
    )


@router.post("/users/login1")
async def log_in(form_data: OAuth2PasswordRequestForm = Depends()):  # TODO: check it and remove it later
    return await JWTAuthentication().login_with_password(form_data.username, form_data.password)


@router.post("/users/login")
async def login(user: UserLogin):
    return await JWTAuthentication().login_with_password(user.username, user.password)


@router.post("/users/token")
async def check_token(user: User = Depends(get_current_user)):
    return TokenData(username=user.username, id=user.id)


@router.get('/users/me')
async def profile(user: User = Depends(get_current_user)):
    return UserProfile.model_validate(user.model_dump())


app.include_router(router)
