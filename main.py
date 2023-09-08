from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.results import InsertOneResult

from dependencies import depends
from models.entities.users import User
from models.schemas.user.user_signup import UserSignUp
from fastapi.exceptions import HTTPException
from core.auth.jwt_authentication import JWTAuthentication
from fastapi.security import OAuth2PasswordRequestForm


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Let's be happy."}


@app.get("/hello/{name}")
async def say_hello(name: str, message: str = ''):
    message = 'you said ' + message if message else ''

    resp = {
        'message': f"Hello {name}. It's working bro ^_^. {message}"
    }
    response = JSONResponse(resp, 200)

    return response


@app.post("/users/signup")
async def sign_up(user_info: UserSignUp, db: AsyncIOMotorDatabase = Depends(depends.get_main_db)):
    # TODO: move it to handler or sth, validate basic password rules, add response model, check email, etc
    existing = await db.users.find_one({"username": user_info.username})
    if existing:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {"message": "This user exists! Try other usernames"},
        )
    user_info.password = JWTAuthentication.hash_password(user_info.password)
    user = User.model_validate(user_info.model_dump())
    result: InsertOneResult = await db.users.insert_one(user.model_dump())
    return JSONResponse(
        {"success": result.acknowledged, "_id": str(result.inserted_id) if result.inserted_id else None},
        status.HTTP_201_CREATED,
    )


@app.post("/users/login")
async def log_in(form_data=Depends(OAuth2PasswordRequestForm)):
    user = JWTAuthentication().get_user()