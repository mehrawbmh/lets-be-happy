from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database.mongo import MongoClient
from app.core.enum.event_types import EventTypes
from app.dependencies.database import get_main_db
from app.endpoints.tasks import router as tasks_router
from app.endpoints.users import router as users_router

router = APIRouter(prefix='/api')


@router.get("/")
async def root():
    return {"message": "Let's be happy yo."}


@router.get("/hello/{name}")
async def health_test(name: str, message: str = '', db: AsyncIOMotorDatabase = Depends(get_main_db)):
    print('new version')
    message = 'you said ' + message if message else ''
    resp = {
        'message': f"Hello {name}. It seems working fine ^_^. {message}"
    }
    return JSONResponse(resp, 200)


router.include_router(users_router)
router.include_router(tasks_router)

app = FastAPI()
app.include_router(router)
app.add_event_handler(EventTypes.STARTUP, MongoClient.crete_indexes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
