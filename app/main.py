from fastapi import FastAPI, Depends, status, APIRouter
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.auth.jwt_authentication import JWTAuthentication
from app.core.enum.access_levels import AccessLevel
from app.dependencies.database import get_main_db
from app.dependencies.user import get_current_user, get_admin_user, get_staff_user
from app.models.entities.users import User
from app.models.schemas.auth.token_data import TokenData
from app.models.schemas.task.task_create import CreateTask
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
    return {"message": "Let's be happy yo."}


@router.get("/hello/{name}")
async def health_test(name: str, message: str = '', db: AsyncIOMotorDatabase = Depends(get_main_db)):
    print('role:', AccessLevel.USER.value)
    test_recode = await db.users.find_one({})
    print('test:', test_recode, sep=' ')
    message = 'you said ' + message if message else ''

    resp = {
        'message': f"Hello {name}. It seems working fine ^_^. {message}"
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
    result = await user.insert()
    return JSONResponse(
        {"success": result.acknowledged, "_id": str(result.inserted_id) if result.inserted_id else None},
        status.HTTP_201_CREATED,
    )


@router.post("/users/login")
async def login(user: UserLogin):
    return await JWTAuthentication().login_with_password(user.username, user.password)


@router.post("/users/token")
async def check_token(user: User = Depends(get_current_user)):
    return TokenData(username=user.username, id=user.id)


@router.get('/users/me')
async def profile(user: User = Depends(get_current_user)):
    return UserProfile.model_validate(user.model_dump())


@router.get('/users/list')
async def list_users(user: User = Depends(get_admin_user), db: AsyncIOMotorDatabase = Depends(get_main_db)):
    users = db.users.find({})
    final = []
    for user in await users.to_list(length=100):
        user = User.model_validate({**user, 'id': str(user['_id'])})
        final.append(user)

    return final


@router.post('/tasks/create')
async def create_task(task_input: CreateTask, user: User = Depends(get_staff_user),
                      db: AsyncIOMotorDatabase = Depends(get_main_db)):
    print(task_input.model_dump())
    return {'ok': 1}
    # task: Task = Task.model_validate(task_input.model_dump())


app.include_router(router)
